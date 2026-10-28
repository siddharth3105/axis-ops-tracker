"""
AI Call Session Models
Stores every AI call conversation with full transcript
"""
from app import db
from datetime import datetime


class AICallSession(db.Model):
    """One AI call session per employee interaction"""
    __tablename__ = 'ai_call_sessions'

    id              = db.Column(db.Integer, primary_key=True)
    employee_id     = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    call_purpose    = db.Column(db.String(200))          # e.g. "Attendance Follow-up"
    call_status     = db.Column(db.String(30), default='In Progress')  # In Progress / Completed / Aborted
    started_at      = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at        = db.Column(db.DateTime)
    duration_seconds= db.Column(db.Integer, default=0)
    turn_count      = db.Column(db.Integer, default=0)   # how many back-and-forths
    summary         = db.Column(db.Text)                  # AI-generated summary
    outcome         = db.Column(db.String(100))           # Available / On Leave / Sick / Unresponsive
    conducted_by    = db.Column(db.String(100), default='AI Assistant')
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to messages
    messages = db.relationship('AICallMessage', backref='session',
                                lazy=True, cascade='all, delete-orphan',
                                order_by='AICallMessage.sequence')

    def to_dict(self):
        return {
            'id':               self.id,
            'employee_id':      self.employee_id,
            'call_purpose':     self.call_purpose or '',
            'call_status':      self.call_status,
            'started_at':       self.started_at.isoformat() if self.started_at else None,
            'ended_at':         self.ended_at.isoformat()   if self.ended_at   else None,
            'duration_seconds': self.duration_seconds or 0,
            'turn_count':       self.turn_count or 0,
            'summary':          self.summary or '',
            'outcome':          self.outcome or '',
            'conducted_by':     self.conducted_by or 'AI Assistant',
        }


class AICallMessage(db.Model):
    """One message (turn) in an AI call conversation"""
    __tablename__ = 'ai_call_messages'

    id         = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('ai_call_sessions.id'), nullable=False)
    sequence   = db.Column(db.Integer, default=0)          # 1, 2, 3 ... turn order
    role       = db.Column(db.String(10))                  # 'user' or 'assistant'
    content    = db.Column(db.Text, nullable=False)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':        self.id,
            'session_id':self.session_id,
            'sequence':  self.sequence,
            'role':      self.role,
            'content':   self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
        }
