
import React, { useState, useEffect } from 'react';
import { Table, Button, Card, Row, Col, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';

const ReportSeries = () => {
  const [reportSeries, setReportSeries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReportSeries = async () => {
      try {
        const response = await axios.get('/report-series/');
        setReportSeries(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching report series:', err);
        setError('Failed to load report series. Please try again later.');
        setLoading(false);
      }
    };

    fetchReportSeries();
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
          <h1>Report Series</h1>
        </Col>
        <Col xs="auto">
          <Button variant="primary">Add Report Series</Button>
        </Col>
      </Row>

      <Card>
        <Card.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>ID</th>
                <th>Series Code</th>
                <th>Series Name</th>
                <th>Filing Frequency</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reportSeries.map((series) => (
                <tr key={series.id}>
                  <td>{series.id}</td>
                  <td>{series.series_code}</td>
                  <td>{series.series_name}</td>
                  <td>{series.filing_frequency}</td>
                  <td>
                    <span className={`badge bg-${series.status === 'active' ? 'success' : 'danger'}`}>
                      {series.status}
                    </span>
                  </td>
                  <td>
                    <Button 
                      variant="info" 
                      size="sm" 
                      className="me-2"
                      onClick={() => window.location.href = `/report-series/${series.id}`}
                    >
                      View
                    </Button>
                    <Button variant="warning" size="sm" className="me-2">Edit</Button>
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

export default ReportSeries;
