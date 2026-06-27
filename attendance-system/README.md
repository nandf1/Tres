# Company Attendance System

A comprehensive attendance tracking system for companies with both backend API and frontend interface.

## Features

- **Dashboard**: View real-time attendance statistics and metrics
- **Employee Management**: Add, view, and manage employee information
- **Attendance Tracking**: Check-in/check-out functionality with timestamps
- **Leave Requests**: Submit, approve, and reject leave requests
- **Reports**: Generate attendance reports and statistics

## Tech Stack

### Backend
- Flask (Python web framework)
- SQLAlchemy (ORM)
- SQLite Database
- RESTful API

### Frontend
- React 18
- React Router
- Axios for API calls
- Modern CSS with responsive design

## Project Structure

```
attendance-system/
├── backend/
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   │   ├── Dashboard.js
    │   │   ├── Employees.js
    │   │   ├── Attendance.js
    │   │   └── LeaveRequests.js
    │   ├── services/
    │   │   └── api.js      # API service layer
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    └── package.json
```

## Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd attendance-system/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd attendance-system/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Companies
- `GET /api/companies` - Get all companies
- `POST /api/companies` - Create a new company

### Departments
- `GET /api/departments` - Get all departments
- `POST /api/departments` - Create a new department

### Employees
- `GET /api/employees` - Get all employees
- `GET /api/employees/:id` - Get specific employee
- `POST /api/employees` - Create a new employee

### Attendance
- `GET /api/attendance` - Get attendance records (with filters)
- `POST /api/attendance/check-in` - Record check-in
- `POST /api/attendance/check-out` - Record check-out
- `PUT /api/attendance/:id` - Update attendance record

### Leave Requests
- `GET /api/leave-requests` - Get all leave requests
- `POST /api/leave-requests` - Create leave request
- `POST /api/leave-requests/:id/approve` - Approve request
- `POST /api/leave-requests/:id/reject` - Reject request

### Statistics
- `GET /api/statistics/attendance` - Get attendance statistics

## Usage

1. **Start the backend server** first (runs on port 5000)
2. **Start the frontend** (runs on port 3000)
3. Open your browser to `http://localhost:3000`
4. Use the navigation menu to access different features:
   - Dashboard for overview statistics
   - Employees to manage staff
   - Attendance to mark check-in/check-out
   - Leave Requests to manage time-off requests

## Sample Data

The backend automatically initializes with sample data:
- 1 Company: "Tech Corp"
- 2 Departments: "IT" and "HR"
- 2 Employees: John Doe and Jane Smith

## License

MIT License
