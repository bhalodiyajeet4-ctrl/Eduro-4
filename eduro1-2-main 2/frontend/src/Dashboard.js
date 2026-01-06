import React, { useState, useEffect } from 'react';
import { Line, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { getDashboardStats } from './api';
import './Dashboard.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement);

function Dashboard({ userType, onLogout }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const userData = JSON.parse(localStorage.getItem('user_data') || '{}');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getDashboardStats(userType);
        setStats(data);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, [userType]);

  const handleLogout = () => {
    localStorage.clear();
    onLogout();
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>SIMS - {userType.toUpperCase()} Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {userData.full_name}</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <div className="dashboard-content">
        {userType === 'admin' && <AdminDashboard stats={stats} />}
        {userType === 'teacher' && <TeacherDashboard stats={stats} />}
        {userType === 'student' && <StudentDashboard stats={stats} />}
      </div>
    </div>
  );
}

function AdminDashboard({ stats }) {
  const attendanceData = {
    labels: stats.attendance_trends?.dates || [],
    datasets: [{
      label: 'Attendance %',
      data: stats.attendance_trends?.percentages || [],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1,
    }],
  };

  const resultData = {
    labels: ['Pass', 'Fail'],
    datasets: [{
      data: [stats.result_distribution?.pass_count || 0, stats.result_distribution?.fail_count || 0],
      backgroundColor: ['#4CAF50', '#f44336'],
    }],
  };

  return (
    <>
      <div className="stats-grid">
        <StatCard title="Total Students" value={stats.total_students} color="#2196F3" />
        <StatCard title="Total Teachers" value={stats.total_teachers} color="#4CAF50" />
        <StatCard title="Avg Attendance" value={`${stats.avg_attendance}%`} color="#FF9800" />
        <StatCard title="Upcoming Events" value={stats.upcoming_events} color="#9C27B0" />
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Attendance Trends</h3>
          <Line data={attendanceData} options={{ maintainAspectRatio: false }} />
        </div>
        <div className="chart-card">
          <h3>Result Distribution</h3>
          <Pie data={resultData} options={{ maintainAspectRatio: false }} />
        </div>
      </div>

      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <button className="action-btn">Add Student</button>
        <button className="action-btn">Add Teacher</button>
        <button className="action-btn">Create Event</button>
      </div>
    </>
  );
}

function TeacherDashboard({ stats }) {
  return (
    <>
      <div className="stats-grid">
        <StatCard title="Total Students" value={stats.total_students} color="#2196F3" />
        <StatCard title="Avg Attendance" value={`${stats.avg_attendance}%`} color="#4CAF50" />
        <StatCard title="Pending Results" value={stats.pending_results} color="#FF9800" />
      </div>

      <div className="section">
        <h3>My Assigned Subjects</h3>
        <div className="subject-list">
          {stats.subjects?.map((subject) => (
            <div key={subject.id} className="subject-card">
              <strong>{subject.code}</strong> - {subject.name}
            </div>
          ))}
        </div>
      </div>

      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <button className="action-btn">Mark Attendance</button>
        <button className="action-btn">Enter Results</button>
      </div>
    </>
  );
}

function StudentDashboard({ stats }) {
  const performanceData = {
    labels: stats.subjects?.map(s => s.subject_name) || [],
    datasets: [{
      label: 'Attendance %',
      data: stats.subjects?.map(s => s.percentage) || [],
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
    }],
  };

  return (
    <>
      <div className="stats-grid">
        <StatCard title="Overall Attendance" value={`${stats.overall_attendance}%`} color="#2196F3" />
        <StatCard title="Avg Percentage" value={`${stats.avg_percentage}%`} color="#4CAF50" />
        <StatCard title="Overall Grade" value={stats.overall_grade} color="#FF9800" />
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Subject-wise Attendance</h3>
          <Line data={performanceData} options={{ maintainAspectRatio: false }} />
        </div>
      </div>

      <div className="data-tables">
        <div className="table-card">
          <h3>Attendance Summary</h3>
          <table>
            <thead>
              <tr>
                <th>Subject</th>
                <th>Present</th>
                <th>Total</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              {stats.subjects?.map((subject, idx) => (
                <tr key={idx}>
                  <td>{subject.subject_name}</td>
                  <td>{subject.present_count}</td>
                  <td>{subject.total_count}</td>
                  <td style={{ color: subject.percentage < 75 ? 'red' : 'green' }}>
                    {subject.percentage}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="table-card">
          <h3>Latest Results</h3>
          <table>
            <thead>
              <tr>
                <th>Subject</th>
                <th>Internal</th>
                <th>External</th>
                <th>Total</th>
                <th>Grade</th>
              </tr>
            </thead>
            <tbody>
              {stats.results?.map((result, idx) => (
                <tr key={idx}>
                  <td>{result.subject_name}</td>
                  <td>{result.internal_marks}/30</td>
                  <td>{result.external_marks}/70</td>
                  <td>{result.total_marks}/100</td>
                  <td><span className={`grade grade-${result.grade.replace('+', 'plus')}`}>{result.grade}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

function StatCard({ title, value, color }) {
  return (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <div className="stat-title">{title}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
}

export default Dashboard;
