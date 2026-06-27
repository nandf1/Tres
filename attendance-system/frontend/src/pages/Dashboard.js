import React from 'react';

const Dashboard = () => {
  const [stats, setStats] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/statistics/attendance');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Employees</h3>
          <p className="stat-value">{stats?.total_employees || 0}</p>
        </div>
        <div className="stat-card present">
          <h3>Present Today</h3>
          <p className="stat-value">{stats?.present_today || 0}</p>
        </div>
        <div className="stat-card absent">
          <h3>Absent Today</h3>
          <p className="stat-value">{stats?.absent_today || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Attendance Rate</h3>
          <p className="stat-value">{stats?.attendance_rate_today || 0}%</p>
        </div>
      </div>
      
      <div className="weekly-stats">
        <h2>Weekly Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Records</h3>
            <p className="stat-value">{stats?.weekly_stats?.total_records || 0}</p>
          </div>
          <div className="stat-card present">
            <h3>Present</h3>
            <p className="stat-value">{stats?.weekly_stats?.present || 0}</p>
          </div>
          <div className="stat-card late">
            <h3>Late</h3>
            <p className="stat-value">{stats?.weekly_stats?.late || 0}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
