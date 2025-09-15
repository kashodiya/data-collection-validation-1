





























































import React, { useContext, useState, useEffect } from 'react';
import { Row, Col, Card, Button, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Dashboard = () => {
  const { currentUser, hasRole } = useContext(AuthContext);
  const [stats, setStats] = useState({
    institutions: 0,
    reportSeries: 0,
    submissions: 0,
    pendingValidations: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // In a real implementation, we would fetch actual statistics
        // For now, we'll use placeholder data
        
        // Simulate API calls
        setLoading(true);
        
        // For external users, we would only fetch their institution's data
        if (currentUser.role === 'external') {
          setStats({
            institutions: 1,
            reportSeries: 3,
            submissions: 5,
            pendingValidations: 2
          });
        } else {
          // For analysts and admins, we would fetch all data
          setStats({
            institutions: 3,
            reportSeries: 3,
            submissions: 12,
            pendingValidations: 4
          });
        }
        
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Failed to load dashboard data. Please try again later.');
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [currentUser]);

  return (
    <div>
      <h1 className="mb-4">Dashboard</h1>
      
      {error && <Alert variant="danger">{error}</Alert>}
      
      <Row className="mb-4">
        <Col md={3}>
          <Card className="dashboard-card h-100">
            <Card.Body className="text-center">
              <h2>{stats.institutions}</h2>
              <p>Institutions</p>
              <Link to="/institutions">
                <Button variant="outline-primary">View Institutions</Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3}>
          <Card className="dashboard-card h-100">
            <Card.Body className="text-center">
              <h2>{stats.reportSeries}</h2>
              <p>Report Series</p>
              <Link to="/report-series">
                <Button variant="outline-primary">View Report Series</Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3}>
          <Card className="dashboard-card h-100">
            <Card.Body className="text-center">
              <h2>{stats.submissions}</h2>
              <p>Submissions</p>
              <Link to="/submissions">
                <Button variant="outline-primary">View Submissions</Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3}>
          <Card className="dashboard-card h-100">
            <Card.Body className="text-center">
              <h2>{stats.pendingValidations}</h2>
              <p>Pending Validations</p>
              <Link to="/submissions">
                <Button variant="outline-warning">View Pending</Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <Row className="mb-4">
        <Col md={6}>
          <Card className="h-100">
            <Card.Header>Quick Actions</Card.Header>
            <Card.Body>
              <div className="d-grid gap-2">
                <Link to="/submissions/upload">
                  <Button variant="primary" className="w-100">Upload New Submission</Button>
                </Link>
                
                <Link to="/forms">
                  <Button variant="secondary" className="w-100">Download Forms</Button>
                </Link>
                
                {hasRole('analyst') && (
                  <Link to="/validation/rules">
                    <Button variant="info" className="w-100">Manage Validation Rules</Button>
                  </Link>
                )}
              </div>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={6}>
          <Card className="h-100">
            <Card.Header>Recent Activity</Card.Header>
            <Card.Body>
              <p className="text-muted">No recent activity to display.</p>
              {/* In a real implementation, we would display recent activity here */}
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      {hasRole('admin') && (
        <Row>
          <Col>
            <Card>
              <Card.Header>Admin Actions</Card.Header>
              <Card.Body>
                <div className="d-grid gap-2">
                  <Button variant="danger">System Configuration</Button>
                  <Button variant="warning">User Management</Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default Dashboard;





























































