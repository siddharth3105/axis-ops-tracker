"""
Employee Data Models
"""
from app import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employees'

    id                   = db.Column(db.Integer, primary_key=True)
    employee_id          = db.Column(db.String(20), unique=True, nullable=False)
    name                 = db.Column(db.String(100), nullable=False)
    email                = db.Column(db.String(120), unique=True, nullable=False)
    mobile               = db.Column(db.String(15))
    shift                = db.Column(db.String(50))
    weekoff_day          = db.Column(db.String(20))
    supervisor           = db.Column(db.String(100))
    status               = db.Column(db.String(20), default='Active')
    is_resident          = db.Column(db.Boolean, default=False)
    is_supervisor        = db.Column(db.Boolean, default=False)
    supervisor_email     = db.Column(db.String(120))
    work_site            = db.Column(db.String(100))
    date_of_joining      = db.Column(db.Date)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)
    user_id              = db.Column(db.String(50))
    accommodation        = db.Column(db.String(100))
    accommodation_status = db.Column(db.String(50))
    training_date        = db.Column(db.Date)

    performance = db.relationship('Performance', backref='employee',
                                  lazy=True, cascade='all, delete-orphan')
    payments    = db.relationship('Payment',     backref='employee',
                                  lazy=True, cascade='all, delete-orphan')
    attendance  = db.relationship('Attendance',  backref='employee',
                                  lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Employee {self.employee_id}: {self.name}>'

    def to_dict(self):
        return {
            'id':                   self.id,
            'employee_id':          self.employee_id,
            'name':                 self.name,
            'email':                self.email,
            'mobile':               self.mobile or '',
            'shift':                self.shift or '',
            'weekoff_day':          self.weekoff_day or '',
            'supervisor':           self.supervisor or '',
            'status':               self.status or 'Active',
            'is_resident':          bool(self.is_resident),
            'is_supervisor':        bool(self.is_supervisor),
            'supervisor_email':     self.supervisor_email or '',
            'work_site':            self.work_site or '',
            'date_of_joining':      self.date_of_joining.isoformat() if self.date_of_joining else None,
            'created_at':           self.created_at.isoformat() if self.created_at else None,
            'user_id':              self.user_id or '',
            'accommodation':        self.accommodation or '',
            'accommodation_status': self.accommodation_status or '',
            'training_date':        self.training_date.isoformat() if self.training_date else None,
        }


class Performance(db.Model):
    __tablename__ = 'performance'

    id                    = db.Column(db.Integer, primary_key=True)
    employee_id           = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    total_days_worked     = db.Column(db.Integer, default=0)
    total_production_hours= db.Column(db.Float,   default=0.0)
    quality_percentage    = db.Column(db.Float,   default=0.0)
    total_videos          = db.Column(db.Integer, default=0)
    recorded_date         = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':                     self.id,
            'employee_id':            self.employee_id,
            'total_days_worked':      int(self.total_days_worked or 0),
            'total_production_hours': round(float(self.total_production_hours or 0), 2),
            'quality_percentage':     round(float(self.quality_percentage or 0), 2),
            'total_videos':           int(self.total_videos or 0),
            'recorded_date':          self.recorded_date.isoformat() if self.recorded_date else None,
        }


class Payment(db.Model):
    __tablename__ = 'payments'

    id                 = db.Column(db.Integer, primary_key=True)
    employee_id        = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    payment_date       = db.Column(db.Date)
    hours_processed    = db.Column(db.Float, default=0.0)
    amount_transferred = db.Column(db.Float, default=0.0)
    last_payment_date  = db.Column(db.Date)
    payment_status     = db.Column(db.String(20), default='Pending')
    created_at         = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':                 self.id,
            'employee_id':        self.employee_id,
            'payment_date':       self.payment_date.isoformat() if self.payment_date else None,
            'hours_processed':    round(float(self.hours_processed or 0), 2),
            'amount_transferred': round(float(self.amount_transferred or 0), 2),
            'last_payment_date':  self.last_payment_date.isoformat() if self.last_payment_date else None,
            'payment_status':     self.payment_status or 'Pending',
            'created_at':         self.created_at.isoformat() if self.created_at else None,
        }


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id           = db.Column(db.Integer, primary_key=True)
    employee_id  = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date         = db.Column(db.Date, nullable=False)
    status       = db.Column(db.String(20), default='Present')
    hours_worked = db.Column(db.Float, default=0.0)
    notes        = db.Column(db.Text)

    def to_dict(self):
        return {
            'id':           self.id,
            'employee_id':  self.employee_id,
            'date':         self.date.isoformat() if self.date else None,
            'status':       self.status or 'Present',
            'hours_worked': round(float(self.hours_worked or 0), 2),
            'notes':        self.notes or '',
        }
