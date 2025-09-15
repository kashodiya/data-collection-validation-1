
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Row, Col, Button, ListGroup, Badge, Spinner, Alert, Tab, Tabs } from 'react-bootstrap';
import axios from 'axios';

const InstitutionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [institution, setInstitution] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loadingSubmissions, setLoadingSubmissions] = useState(true);

  useEffect(() => {
    const fetchInstitution = async () => {
      try {
        const response = await axios.get(`/institutions/${id}`);
        setInstitution(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching institution details:', err);
        setError('Failed to load institution details. Please try again later.');
        setLoading(false);
      }
    };

    const fetchSubmissions = async () => {
      try {
        // This endpoint might need to be adjusted based on your API
        const response = await axios.get(`/submissions?institution_id=${id}`);
        setSubmissions(response.data);
        setLoadingSubmissions(false);
      } catch (err) {
        console.error('Error fetching institution submissions:', err);
        setLoadingSubmissions(false);
      }
    };

    fetchInstitution();
    fetchSubmissions();
  }, [id]);

  const handleBack = () => {
    navigate('/institutions');
  };

  if (loading) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger">
        {error}
      </Alert>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Institution Details</h1>
        <Button variant="secondary" onClick={handleBack}>Back to Institutions</Button>
      </div>

      <Card className="mb-4">
        <Card.Header as="h5">
          {institution.name}
          <Badge bg={institution.status === 'active' ? 'success' : 'danger'} className="ms-2">
            {institution.status}
          </Badge>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={6}>
              <ListGroup variant="flush">
                <ListGroup.Item>
                  <strong>RSSD ID:</strong> {institution.rssd_id}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Institution Type:</strong> {institution.institution_type}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Contact Information:</strong> {institution.contact_info}
                </ListGroup.Item>
              </ListGroup>
            </Col>
            <Col md={6}>
              <ListGroup variant="flush">
                <ListGroup.Item>
                  <strong>ID:</strong> {institution.id}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Created:</strong> {new Date(institution.created_at).toLocaleString()}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Last Updated:</strong> {new Date(institution.updated_at).toLocaleString()}
                </ListGroup.Item>
              </ListGroup>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <Tabs defaultActiveKey="submissions" className="mb-3">
        <Tab eventKey="submissions" title="Submissions">
          <Card>
            <Card.Body>
              {loadingSubmissions ? (
                <div className="text-center my-3">
                  <Spinner animation="border" size="sm" />
                </div>
              ) : submissions.length > 0 ? (
                <table className="table table-striped">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Report Series</th>
                      <th>Reporting Date</th>
                      <th>Submission Date</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {submissions.map(submission => (
                      <tr key={submission.id}>
                        <td>{submission.id}</td>
                        <td>{submission.report_series_name}</td>
                        <td>{new Date(submission.reporting_date).toLocaleDateString()}</td>
                        <td>{new Date(submission.submission_date).toLocaleDateString()}</td>
                        <td>
                          <Badge bg={
                            submission.status === 'submitted' ? 'primary' :
                            submission.status === 'validated' ? 'success' :
                            submission.status === 'rejected' ? 'danger' : 'warning'
                          }>
                            {submission.status}
                          </Badge>
                        </td>
                        <td>
                          <Button variant="info" size="sm" className="me-2">View</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <Alert variant="info">No submissions found for this institution.</Alert>
              )}
            </Card.Body>
          </Card>
        </Tab>
        <Tab eventKey="reports" title="Assigned Reports">
          <Card>
            <Card.Body>
              <Alert variant="info">Report series assignment functionality coming soon.</Alert>
            </Card.Body>
          </Card>
        </Tab>
        <Tab eventKey="users" title="Users">
          <Card>
            <Card.Body>
              <Alert variant="info">User management functionality coming soon.</Alert>
            </Card.Body>
          </Card>
        </Tab>
      </Tabs>
    </div>
  );
};

export default InstitutionDetail;
