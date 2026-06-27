import React from 'react';

const Attendance = () => {
  const [attendance, setAttendance] = React.useState([]);
  const [employees, setEmployees] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [selectedEmployee, setSelectedEmployee] = React.useState('');
  const [message, setMessage] = React.useState({ type: '', text: '' });

  React.useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [attendanceRes, employeesRes] = await Promise.all([
        fetch('http://localhost:5000/api/attendance'),
        fetch('http://localhost:5000/api/employees')
      ]);
      const attendanceData = await attendanceRes.json();
      const employeesData = await employeesRes.json();
      setAttendance(attendanceData);
      setEmployees(employeesData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckIn = async () => {
    if (!selectedEmployee) {
      setMessage({ type: 'error', text: 'Please select an employee' });
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/attendance/check-in', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employee_id: parseInt(selectedEmployee) })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setMessage({ type: 'success', text: `Check-in successful for ${data.date}` });
        fetchData();
      } else {
        setMessage({ type: 'error', text: data.error || 'Check-in failed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Check-in failed' });
    }
  };

  const handleCheckOut = async () => {
    if (!selectedEmployee) {
      setMessage({ type: 'error', text: 'Please select an employee' });
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/attendance/check-out', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employee_id: parseInt(selectedEmployee) })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setMessage({ type: 'success', text: `Check-out successful for ${data.date}` });
        fetchData();
      } else {
        setMessage({ type: 'error', text: data.error || 'Check-out failed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Check-out failed' });
    }
  };

  if (loading) {
    return <div>Loading attendance records...</div>;
  }

  return (
    <div className="attendance-page">
      <h1>Attendance Management</h1>

      <div className="attendance-actions">
        <div className="action-card">
          <h2>Mark Attendance</h2>
          <select 
            value={selectedEmployee} 
            onChange={(e) => setSelectedEmployee(e.target.value)}
            className="form-select"
          >
            <option value="">Select Employee</option>
            {employees.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.first_name} {emp.last_name} ({emp.employee_id})
              </option>
            ))}
          </select>
          
          <div className="action-buttons">
            <button onClick={handleCheckIn} className="btn-success">
              Check In
            </button>
            <button onClick={handleCheckOut} className="btn-warning">
              Check Out
            </button>
          </div>

          {message.text && (
            <div className={`message ${message.type}`}>{message.text}</div>
          )}
        </div>
      </div>

      <div className="table-container">
        <h2>Recent Attendance Records</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Employee</th>
              <th>Check In</th>
              <th>Check Out</th>
              <th>Status</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {attendance.map((record) => (
              <tr key={record.id}>
                <td>{record.date}</td>
                <td>{record.employee_name}</td>
                <td>{record.check_in ? new Date(record.check_in).toLocaleTimeString() : '-'}</td>
                <td>{record.check_out ? new Date(record.check_out).toLocaleTimeString() : '-'}</td>
                <td>
                  <span className={`status-badge ${record.status}`}>
                    {record.status}
                  </span>
                </td>
                <td>{record.notes || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Attendance;
