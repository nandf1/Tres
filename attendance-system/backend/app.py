"""
Attendance System Backend - Flask API
A comprehensive attendance tracking system for companies
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy(app)

# ==================== MODELS ====================

class Company(db.Model):
    """Company model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employees = db.relationship('Employee', backref='company', lazy=True)
    departments = db.relationship('Department', backref='company', lazy=True)

class Department(db.Model):
    """Department model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employees = db.relationship('Employee', backref='department', lazy=True)

class Employee(db.Model):
    """Employee model"""
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    position = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    hire_date = db.Column(db.Date, default=date.today)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    attendance_records = db.relationship('AttendanceRecord', backref='employee', lazy=True)

class AttendanceRecord(db.Model):
    """Attendance record model"""
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='present')  # present, absent, late, half_day, leave
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='unique_employee_date'),)

class LeaveRequest(db.Model):
    """Leave request model"""
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)  # sick, vacation, personal, etc.
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('employee.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== HELPER FUNCTIONS ====================

def init_db():
    """Initialize database with sample data"""
    db.create_all()
    
    # Check if data already exists
    if Company.query.first() is None:
        # Create sample company
        company = Company(name="Tech Corp", address="123 Business St, Tech City")
        db.session.add(company)
        db.session.commit()
        
        # Create sample departments
        it_dept = Department(name="IT", company_id=company.id)
        hr_dept = Department(name="HR", company_id=company.id)
        db.session.add_all([it_dept, hr_dept])
        db.session.commit()
        
        # Create sample employees
        emp1 = Employee(
            employee_id="EMP001",
            first_name="John",
            last_name="Doe",
            email="john.doe@techcorp.com",
            phone="555-0101",
            position="Software Engineer",
            department_id=it_dept.id,
            company_id=company.id
        )
        
        emp2 = Employee(
            employee_id="EMP002",
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@techcorp.com",
            phone="555-0102",
            position="HR Manager",
            department_id=hr_dept.id,
            company_id=company.id
        )
        
        db.session.add_all([emp1, emp2])
        db.session.commit()
        
        print("Database initialized with sample data!")

# ==================== ROUTES ====================

@app.route('/')
def index():
    """API welcome endpoint"""
    return jsonify({
        "message": "Welcome to Attendance System API",
        "version": "1.0.0",
        "endpoints": {
            "companies": "/api/companies",
            "employees": "/api/employees",
            "departments": "/api/departments",
            "attendance": "/api/attendance",
            "leave_requests": "/api/leave-requests"
        }
    })

# Company Routes
@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get all companies"""
    companies = Company.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'address': c.address,
        'created_at': c.created_at.isoformat()
    } for c in companies])

@app.route('/api/companies', methods=['POST'])
def create_company():
    """Create a new company"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Company name is required'}), 400
    
    company = Company(
        name=data['name'],
        address=data.get('address', '')
    )
    db.session.add(company)
    db.session.commit()
    
    return jsonify({
        'id': company.id,
        'name': company.name,
        'address': company.address,
        'created_at': company.created_at.isoformat()
    }), 201

# Department Routes
@app.route('/api/departments', methods=['GET'])
def get_departments():
    """Get all departments"""
    departments = Department.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'company_id': d.company_id,
        'created_at': d.created_at.isoformat()
    } for d in departments])

@app.route('/api/departments', methods=['POST'])
def create_department():
    """Create a new department"""
    data = request.get_json()
    if not data or 'name' not in data or 'company_id' not in data:
        return jsonify({'error': 'Department name and company_id are required'}), 400
    
    department = Department(
        name=data['name'],
        company_id=data['company_id']
    )
    db.session.add(department)
    db.session.commit()
    
    return jsonify({
        'id': department.id,
        'name': department.name,
        'company_id': department.company_id,
        'created_at': department.created_at.isoformat()
    }), 201

# Employee Routes
@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get all employees"""
    employees = Employee.query.all()
    return jsonify([{
        'id': e.id,
        'employee_id': e.employee_id,
        'first_name': e.first_name,
        'last_name': e.last_name,
        'email': e.email,
        'phone': e.phone,
        'position': e.position,
        'department_id': e.department_id,
        'company_id': e.company_id,
        'hire_date': e.hire_date.isoformat(),
        'is_active': e.is_active
    } for e in employees])

@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get a specific employee"""
    employee = Employee.query.get_or_404(employee_id)
    return jsonify({
        'id': employee.id,
        'employee_id': employee.employee_id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email,
        'phone': employee.phone,
        'position': employee.position,
        'department_id': employee.department_id,
        'company_id': employee.company_id,
        'hire_date': employee.hire_date.isoformat(),
        'is_active': employee.is_active
    })

@app.route('/api/employees', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.get_json()
    required_fields = ['employee_id', 'first_name', 'last_name', 'email', 'company_id']
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    employee = Employee(
        employee_id=data['employee_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone', ''),
        position=data.get('position', ''),
        department_id=data.get('department_id'),
        company_id=data['company_id'],
        hire_date=datetime.strptime(data.get('hire_date', date.today().isoformat()), '%Y-%m-%d').date() if isinstance(data.get('hire_date'), str) else data.get('hire_date', date.today())
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify({
        'id': employee.id,
        'employee_id': employee.employee_id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email,
        'phone': employee.phone,
        'position': employee.position,
        'department_id': employee.department_id,
        'company_id': employee.company_id,
        'hire_date': employee.hire_date.isoformat(),
        'is_active': employee.is_active
    }), 201

# Attendance Routes
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """Get attendance records with optional filters"""
    employee_id = request.args.get('employee_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = AttendanceRecord.query
    
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if date_from:
        query = query.filter(AttendanceRecord.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        query = query.filter(AttendanceRecord.date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    records = query.order_by(AttendanceRecord.date.desc()).all()
    
    return jsonify([{
        'id': r.id,
        'employee_id': r.employee_id,
        'employee_name': f"{r.employee.first_name} {r.employee.last_name}",
        'date': r.date.isoformat(),
        'check_in': r.check_in.isoformat() if r.check_in else None,
        'check_out': r.check_out.isoformat() if r.check_out else None,
        'status': r.status,
        'notes': r.notes
    } for r in records])

@app.route('/api/attendance/check-in', methods=['POST'])
def check_in():
    """Record employee check-in"""
    data = request.get_json()
    if not data or 'employee_id' not in data:
        return jsonify({'error': 'employee_id is required'}), 400
    
    employee_id = data['employee_id']
    today = date.today()
    
    # Check if record already exists for today
    existing_record = AttendanceRecord.query.filter_by(
        employee_id=employee_id,
        date=today
    ).first()
    
    if existing_record:
        return jsonify({'error': 'Check-in already recorded for today'}), 400
    
    record = AttendanceRecord(
        employee_id=employee_id,
        date=today,
        check_in=datetime.utcnow(),
        status='present'
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'id': record.id,
        'employee_id': record.employee_id,
        'date': record.date.isoformat(),
        'check_in': record.check_in.isoformat(),
        'status': record.status
    }), 201

@app.route('/api/attendance/check-out', methods=['POST'])
def check_out():
    """Record employee check-out"""
    data = request.get_json()
    if not data or 'employee_id' not in data:
        return jsonify({'error': 'employee_id is required'}), 400
    
    employee_id = data['employee_id']
    today = date.today()
    
    record = AttendanceRecord.query.filter_by(
        employee_id=employee_id,
        date=today
    ).first()
    
    if not record:
        return jsonify({'error': 'No check-in record found for today'}), 400
    
    if record.check_out:
        return jsonify({'error': 'Check-out already recorded for today'}), 400
    
    record.check_out = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'id': record.id,
        'employee_id': record.employee_id,
        'date': record.date.isoformat(),
        'check_in': record.check_in.isoformat(),
        'check_out': record.check_out.isoformat(),
        'status': record.status
    })

@app.route('/api/attendance/<int:record_id>', methods=['PUT'])
def update_attendance(record_id):
    """Update attendance record"""
    data = request.get_json()
    record = AttendanceRecord.query.get_or_404(record_id)
    
    if 'status' in data:
        record.status = data['status']
    if 'notes' in data:
        record.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'id': record.id,
        'employee_id': record.employee_id,
        'date': record.date.isoformat(),
        'check_in': record.check_in.isoformat() if record.check_in else None,
        'check_out': record.check_out.isoformat() if record.check_out else None,
        'status': record.status,
        'notes': record.notes
    })

# Leave Request Routes
@app.route('/api/leave-requests', methods=['GET'])
def get_leave_requests():
    """Get all leave requests"""
    employee_id = request.args.get('employee_id')
    status = request.args.get('status')
    
    query = LeaveRequest.query
    
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if status:
        query = query.filter_by(status=status)
    
    requests = query.order_by(LeaveRequest.created_at.desc()).all()
    
    return jsonify([{
        'id': lr.id,
        'employee_id': lr.employee_id,
        'employee_name': f"{lr.employee.first_name} {lr.employee.last_name}",
        'start_date': lr.start_date.isoformat(),
        'end_date': lr.end_date.isoformat(),
        'leave_type': lr.leave_type,
        'reason': lr.reason,
        'status': lr.status,
        'created_at': lr.created_at.isoformat()
    } for lr in requests])

@app.route('/api/leave-requests', methods=['POST'])
def create_leave_request():
    """Create a new leave request"""
    data = request.get_json()
    required_fields = ['employee_id', 'start_date', 'end_date', 'leave_type']
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    leave_request = LeaveRequest(
        employee_id=data['employee_id'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        leave_type=data['leave_type'],
        reason=data.get('reason', '')
    )
    
    db.session.add(leave_request)
    db.session.commit()
    
    return jsonify({
        'id': leave_request.id,
        'employee_id': leave_request.employee_id,
        'start_date': leave_request.start_date.isoformat(),
        'end_date': leave_request.end_date.isoformat(),
        'leave_type': leave_request.leave_type,
        'reason': leave_request.reason,
        'status': leave_request.status
    }), 201

@app.route('/api/leave-requests/<int:request_id>/approve', methods=['POST'])
def approve_leave_request(request_id):
    """Approve a leave request"""
    data = request.get_json()
    leave_request = LeaveRequest.query.get_or_404(request_id)
    
    leave_request.status = 'approved'
    if data and 'approved_by' in data:
        leave_request.approved_by = data['approved_by']
    
    db.session.commit()
    
    return jsonify({
        'id': leave_request.id,
        'status': leave_request.status,
        'message': 'Leave request approved'
    })

@app.route('/api/leave-requests/<int:request_id>/reject', methods=['POST'])
def reject_leave_request(request_id):
    """Reject a leave request"""
    leave_request = LeaveRequest.query.get_or_404(request_id)
    leave_request.status = 'rejected'
    db.session.commit()
    
    return jsonify({
        'id': leave_request.id,
        'status': leave_request.status,
        'message': 'Leave request rejected'
    })

# Statistics Route
@app.route('/api/statistics/attendance', methods=['GET'])
def get_attendance_statistics():
    """Get attendance statistics"""
    today = date.today()
    
    total_employees = Employee.query.filter_by(is_active=True).count()
    present_today = AttendanceRecord.query.filter_by(date=today, status='present').count()
    absent_today = total_employees - present_today
    
    # Get this week's statistics
    from datetime import timedelta
    week_start = today - timedelta(days=today.weekday())
    
    weekly_records = AttendanceRecord.query.filter(
        AttendanceRecord.date >= week_start,
        AttendanceRecord.date <= today
    ).all()
    
    weekly_present = len([r for r in weekly_records if r.status == 'present'])
    weekly_late = len([r for r in weekly_records if r.status == 'late'])
    
    return jsonify({
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'attendance_rate_today': round((present_today / total_employees * 100), 2) if total_employees > 0 else 0,
        'weekly_stats': {
            'total_records': len(weekly_records),
            'present': weekly_present,
            'late': weekly_late
        }
    })

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
