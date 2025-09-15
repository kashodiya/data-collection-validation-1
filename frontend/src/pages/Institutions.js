import React, { useState, useEffect } from 'react';
import { Table, Button, Card, Row, Col, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';

const Institutions = () => {
  const [institutions, setInstitutions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInstitutions = async () => {
      try {
        // Using the baseURL set in AuthContext.js (http://localhost:51209/api/v1)
        const response = await axios.get('/institutions/');
        setInstitutions(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching institutions:', err);
        setError('Failed to load institutions. Please try again later.');
        setLoading(false);
      }
    };

    fetchInstitutions();
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
          <h1>Institutions</h1>
        </Col>
        <Col xs="auto">
          <Button variant="primary">Add Institution</Button>
        </Col>
      </Row>

      <Card>
        <Card.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>ID</th>
                <th>RSSD ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Contact Info</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {institutions.map((institution) => (
                <tr key={institution.id}>
                  <td>{institution.id}</td>
                  <td>{institution.rssd_id}</td>
                  <td>{institution.name}</td>
                  <td>{institution.institution_type}</td>
                  <td>{institution.contact_info}</td>
                  <td>
                    <span className={`badge bg-${institution.status === 'active' ? 'success' : 'danger'}`}>
                      {institution.status}
                    </span>
                  </td>
                  <td>
                    <Button 
                      variant="info" 
                      size="sm" 
                      className="me-2"
                      onClick={() => window.location.href = `/institutions/${institution.id}`}
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

export default Institutions;
