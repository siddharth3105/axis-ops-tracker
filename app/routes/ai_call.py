"""
AI Calling Assistant Routes
Browser-based voice AI using Groq (free forever)
Flow: Browser mic → base64 audio → Whisper (Groq) → text
      → Groq Llama3 chat → AI reply text
      → returned to browser → browser speaks it aloud
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import Employee, AICallSession, AICallMessage
from app import db
from datetime import datetime
import os
import json
import base64
import tempfile

bp = Blueprint('ai_call', __name__, url_prefix='/ai-call')

# ── Groq client (lazy init so missing key doesn't crash app startup) ──────────
_groq_client = None

def get_groq():
    global _groq_client
    if _groq_client is None:
        try:
            from groq import Groq
            api_key = os.environ.get('GROQ_API_KEY', '')
            if not api_key:
                raise ValueError('GROQ_API_KEY not set')
            _groq_client = Groq(api_key=api_key)
        except ImportError:
            raise RuntimeError('groq package not installed. Run: pip install groq')
    return _groq_client


# ── System prompt for the AI calling assistant ────────────────────────────────
SYSTEM_PROMPT = """You are Arya, an AI assistant calling on behalf of Axis Operations Team.
Your job is to have a professional, friendly conversation with employees to check on their 
work status, attendance, and wellbeing.

Guidelines:
- Be warm, professional, and concise — this is a voice call so keep responses SHORT (2-3 sentences max)
- Start by greeting the employee by name and stating the purpose
- Ask about their current status: are they available, on leave, sick, or need follow-up?
- Ask about any attendance issues or concerns
- If they have QC feedback concerns, listen and note them
- End the call professionally, summarize what was discussed
- Always be empathetic and respectful

When you have gathered enough information, include [CALL_OUTCOME: Available/On Leave/Sick/Follow-up Required/Unresponsive] 
at the end of your final message.

Keep each response under 40 words — this is a voice call."""


# ── Pages ─────────────────────────────────────────────────────────────────────

@bp.route('/')
def index():
    return render_template('ai_call.html')


@bp.route('/session/<int:session_id>')
def call_session(session_id):
    session = AICallSession.query.get_or_404(session_id)
    employee = Employee.query.get_or_404(session.employee_id)
    return render_template('ai_call.html',
                           session_id=session_id,
                           employee_name=employee.name)


# ── API: Start a new call session ─────────────────────────────────────────────

@bp.route('/api/start', methods=['POST'])
def start_session():
    """Create a new AI call session for an employee"""
    try:
        data = request.get_json() or {}
        employee_id = int(data.get('employee_id', 0))
        if not employee_id:
            return jsonify({'success': False, 'error': 'employee_id is required'}), 400

        employee = Employee.query.get_or_404(employee_id)
        purpose  = data.get('purpose', 'General Follow-up')

        session = AICallSession(
            employee_id  = employee_id,
            call_purpose = purpose,
            call_status  = 'In Progress',
            started_at   = datetime.utcnow(),
        )
        db.session.add(session)
        db.session.commit()

        # Generate the AI's opening message
        opening = _get_ai_opening(employee.name, purpose)

        # Save as first message
        msg = AICallMessage(
            session_id = session.id,
            sequence   = 1,
            role       = 'assistant',
            content    = opening,
        )
        db.session.add(msg)
        session.turn_count = 1
        db.session.commit()

        return jsonify({
            'success':      True,
            'session_id':   session.id,
            'employee_name':employee.name,
            'opening_message': opening,
            'message':      'Call session started'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


def _get_ai_opening(employee_name, purpose):
    """Generate AI's opening line for the call"""
    try:
        groq = get_groq()
        response = groq.chat.completions.create(
            model='llama3-70b-8192',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user',   'content': f'Start the call. Employee name: {employee_name}. Purpose: {purpose}. Give your opening greeting only.'}
            ],
            max_tokens=80,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Hello {employee_name}, this is Arya calling from Axis Operations. How are you doing today?"


# ── API: Transcribe audio (Whisper via Groq) ──────────────────────────────────

@bp.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """Receive base64 audio from browser, transcribe with Whisper via Groq"""
    try:
        data       = request.get_json() or {}
        audio_b64  = data.get('audio')
        audio_mime = data.get('mime', 'audio/webm')

        if not audio_b64:
            return jsonify({'success': False, 'error': 'No audio data'}), 400

        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_b64)

        # Write to temp file — Groq Whisper needs a file
        suffix = '.webm' if 'webm' in audio_mime else '.wav'
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            groq = get_groq()
            with open(tmp_path, 'rb') as audio_file:
                transcription = groq.audio.transcriptions.create(
                    model='whisper-large-v3',
                    file=audio_file,
                    response_format='text'
                )
            transcript_text = transcription.strip() if isinstance(transcription, str) else transcription
        finally:
            os.unlink(tmp_path)  # cleanup

        if not transcript_text:
            return jsonify({'success': True, 'transcript': '', 'empty': True})

        return jsonify({'success': True, 'transcript': transcript_text})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ── API: Send user message, get AI reply ──────────────────────────────────────

@bp.route('/api/chat', methods=['POST'])
def chat():
    """Send user transcript to Groq, get AI response, save both"""
    try:
        data           = request.get_json() or {}
        session_id     = int(data.get('session_id', 0))
        user_message   = (data.get('message') or '').strip()
        employee_name  = data.get('employee_name', '')

        if not session_id or not user_message:
            return jsonify({'success': False, 'error': 'session_id and message required'}), 400

        call_session = AICallSession.query.get_or_404(session_id)

        # Load full conversation history
        history = AICallMessage.query.filter_by(session_id=session_id).order_by(AICallMessage.sequence).all()
        messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        for h in history:
            messages.append({'role': h.role, 'content': h.content})

        # Add latest user message
        messages.append({'role': 'user', 'content': user_message})

        # Save user message
        next_seq = len(history) + 1
        user_msg = AICallMessage(
            session_id = session_id,
            sequence   = next_seq,
            role       = 'user',
            content    = user_message,
        )
        db.session.add(user_msg)

        # Get AI response from Groq
        groq = get_groq()
        response = groq.chat.completions.create(
            model='llama3-70b-8192',
            messages=messages,
            max_tokens=120,
            temperature=0.7,
        )
        ai_reply = response.choices[0].message.content.strip()

        # Check if AI signalled call outcome
        outcome = None
        import re
        outcome_match = re.search(r'\[CALL_OUTCOME:\s*([^\]]+)\]', ai_reply)
        if outcome_match:
            outcome = outcome_match.group(1).strip()
            ai_reply = re.sub(r'\[CALL_OUTCOME:[^\]]+\]', '', ai_reply).strip()

        # Save AI message
        ai_msg = AICallMessage(
            session_id = session_id,
            sequence   = next_seq + 1,
            role       = 'assistant',
            content    = ai_reply,
        )
        db.session.add(ai_msg)

        # Update session
        call_session.turn_count = next_seq + 1
        if outcome:
            call_session.outcome = outcome

        db.session.commit()

        return jsonify({
            'success':   True,
            'reply':     ai_reply,
            'outcome':   outcome,
            'turn':      next_seq + 1,
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ── API: End call, generate summary ───────────────────────────────────────────

@bp.route('/api/end', methods=['POST'])
def end_call():
    """End call session, generate AI summary, save to followup log"""
    try:
        data       = request.get_json() or {}
        session_id = int(data.get('session_id', 0))
        outcome    = data.get('outcome', '')

        call_session = AICallSession.query.get_or_404(session_id)

        # Calculate duration
        ended_at = datetime.utcnow()
        duration = int((ended_at - call_session.started_at).total_seconds())

        # Get full transcript for summary
        history = AICallMessage.query.filter_by(session_id=session_id).order_by(AICallMessage.sequence).all()
        transcript_text = '\n'.join([f"{m.role.upper()}: {m.content}" for m in history])

        # Generate summary with Groq
        summary = _generate_summary(transcript_text, call_session.call_purpose)

        # Update session
        call_session.ended_at        = ended_at
        call_session.duration_seconds= duration
        call_session.call_status     = 'Completed'
        call_session.summary         = summary
        if outcome:
            call_session.outcome = outcome

        db.session.commit()

        # Also log to FollowUp tracker automatically
        try:
            _auto_log_followup(call_session)
        except Exception:
            pass  # don't fail if followup log fails

        return jsonify({
            'success':  True,
            'summary':  summary,
            'duration': duration,
            'outcome':  call_session.outcome or outcome,
            'turns':    call_session.turn_count,
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


def _generate_summary(transcript, purpose):
    """Ask Groq to summarise the call transcript"""
    try:
        groq = get_groq()
        response = groq.chat.completions.create(
            model='llama3-70b-8192',
            messages=[
                {'role': 'system', 'content': 'You are a call summarizer. Write a concise 2-3 sentence summary of this call transcript. Focus on: what was discussed, employee status, any action items.'},
                {'role': 'user',   'content': f'Call Purpose: {purpose}\n\nTranscript:\n{transcript}'}
            ],
            max_tokens=150,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f'Call completed. Purpose: {purpose}.'


def _auto_log_followup(call_session):
    """Auto-create a FollowUp log entry when call ends"""
    try:
        from app.models.followup import FollowUp, WorkforceStatus
        from datetime import date

        log = FollowUp(
            employee_id   = call_session.employee_id,
            contact_type  = 'Call',
            direction     = 'Outbound',
            status        = 'Reached' if call_session.outcome != 'Unresponsive' else 'No Answer',
            duration_minutes = round((call_session.duration_seconds or 0) / 60, 1),
            notes         = f'[AI Call] {call_session.summary or call_session.call_purpose}',
            contacted_by  = 'AI Assistant',
            follow_up_required = call_session.outcome in ['Follow-up Required', 'Sick'],
        )
        db.session.add(log)

        # Update workforce status
        ws = WorkforceStatus.query.filter_by(employee_id=call_session.employee_id).first()
        if not ws:
            ws = WorkforceStatus(employee_id=call_session.employee_id)
            db.session.add(ws)

        if call_session.outcome:
            ws.current_status   = call_session.outcome
            ws.last_contact_date= date.today()
            ws.status_notes     = call_session.summary or ''
            ws.updated_at       = datetime.utcnow()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


# ── API: Get session history ──────────────────────────────────────────────────

@bp.route('/api/sessions')
def list_sessions():
    """List all call sessions with employee names"""
    try:
        employee_id = request.args.get('employee_id')
        query = db.session.query(
            AICallSession, Employee.name, Employee.employee_id.label('emp_code')
        ).join(Employee, Employee.id == AICallSession.employee_id)

        if employee_id:
            query = query.filter(AICallSession.employee_id == int(employee_id))

        rows = query.order_by(AICallSession.started_at.desc()).limit(100).all()

        result = []
        for s, emp_name, emp_code in rows:
            d = s.to_dict()
            d['employee_name'] = emp_name
            d['employee_code'] = emp_code
            result.append(d)

        return jsonify({'success': True, 'sessions': result, 'count': len(result)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/sessions/<int:session_id>/transcript')
def get_transcript(session_id):
    """Full transcript for a call session"""
    try:
        call_session = AICallSession.query.get_or_404(session_id)
        employee     = Employee.query.get(call_session.employee_id)
        messages     = AICallMessage.query.filter_by(session_id=session_id).order_by(AICallMessage.sequence).all()

        return jsonify({
            'success':      True,
            'session':      call_session.to_dict(),
            'employee_name':employee.name if employee else 'Unknown',
            'messages':     [m.to_dict() for m in messages],
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/sessions/<int:session_id>/delete', methods=['DELETE'])
def delete_session(session_id):
    try:
        s = AICallSession.query.get_or_404(session_id)
        db.session.delete(s)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Session deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/summary')
def call_summary():
    """Dashboard summary stats for AI calls"""
    try:
        from sqlalchemy import func
        total    = AICallSession.query.count()
        completed= AICallSession.query.filter_by(call_status='Completed').count()
        today    = datetime.utcnow().date()
        today_calls = AICallSession.query.filter(
            db.func.date(AICallSession.started_at) == today
        ).count()

        outcomes = db.session.query(
            AICallSession.outcome, func.count(AICallSession.id)
        ).filter(AICallSession.outcome.isnot(None)
        ).group_by(AICallSession.outcome).all()

        return jsonify({
            'success': True,
            'summary': {
                'total_calls':    total,
                'completed':      completed,
                'today_calls':    today_calls,
                'outcomes':       {o: c for o, c in outcomes},
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
