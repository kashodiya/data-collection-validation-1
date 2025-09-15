

import React, { useState, useEffect } from 'react';
import { Table, Button, Card, Row, Col, Spinner, Alert, Badge } from 'react-bootstrap';
import axios from 'axios';

const Submissions = () => {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const response = await axios.get('/submissions/');
        setSubmissions(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching submissions:', err);
        setError('Failed to load submissions. Please try again later.');
        setLoading(false);
      }
    };

    fetchSubmissions();
  }, []);

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
      <Row className="mb-4">
        <Col>
          <h1>Submissions</h1>
        </Col>
        <Col xs="auto">
          <Button variant="primary">Upload New Submission</Button>
        </Col>
      </Row>

      <Card>
        <Card.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>ID</th>
                <th>Institution</th>
                <th>Report Series</th>
                <th>Reporting Date</th>
                <th>Submission Date</th>
                <th>Status</th>
                <th>Validation Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {submissions.map((submission) => (
                <tr key={submission.id}>
                  <td>{submission.id}</td>
                  <td>{submission.institution_name}</td>
                  <td>{submission.report_series_name}</td>
                  <td>{new Date(submission.reporting_date).toLocaleDateString()}</td>
                  <td>{new Date(submission.submission_date).toLocaleDateString()}</td>
                  <td>
                    <Badge bg={
                      submission.status === 'submitted' ? 'primary' :
                      submission.status === 'approved' ? 'success' :
                      submission.status === 'rejected' ? 'danger' : 'warning'
                    }>
                      {submission.status}
                    </Badge>
                  </td>
                  <td>
                    <Badge bg={
                      submission.validation_status === 'passed' ? 'success' :
                      submission.validation_status === 'failed' ? 'danger' : 'warning'
                    }>
                      {submission.validation_status}
                    </Badge>
                  </td>
                  <td>
                    <Button 
                      variant="info" 
                      size="sm" 
                      className="me-2"
                      onClick={() => window.location.href = `/submissions/${submission.id}`}
                    >
                      View
                    </Button>
                    <Button variant="warning" size="sm" className="me-2">Validate</Button>
                    <Button variant="danger" size="sm">Delete</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Submissions;

