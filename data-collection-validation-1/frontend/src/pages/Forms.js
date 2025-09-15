


import React, { useState, useEffect } from 'react';
import { Table, Button, Card, Row, Col, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';

const Forms = () => {
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchForms = async () => {
      try {
        const response = await axios.get('/forms/');
        setForms(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching forms:', err);
        setError('Failed to load forms. Please try again later.');
        setLoading(false);
      }
    };

    fetchForms();
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

  // Sample forms data if API doesn't return any
  const sampleForms = [
    {
      id: 1,
      series_code: 'FR Y-9C',
      form_name: 'Consolidated Financial Statements for Holding Companies',
      form_pdf_path: '/forms/FR_Y-9C_202403.pdf',
      instructions_pdf_path: '/forms/FR_Y-9C_instructions_202403.pdf',
      effective_date: '2024-03-31',
      end_date: null
    },
    {
      id: 2,
      series_code: 'FFIEC 031',
      form_name: 'Consolidated Reports of Condition and Income for Banks',
      form_pdf_path: '/forms/FFIEC_031_202403.pdf',
      instructions_pdf_path: '/forms/FFIEC_031_instructions_202403.pdf',
      effective_date: '2024-03-31',
      end_date: null
    },
    {
      id: 3,
      series_code: 'FR 2052a',
      form_name: 'Complex Institution Liquidity Monitoring Report',
      form_pdf_path: '/forms/FR_2052a_202401.pdf',
      instructions_pdf_path: '/forms/FR_2052a_instructions_202401.pdf',
      effective_date: '2024-01-31',
      end_date: null
    }
  ];

  const displayForms = forms.length > 0 ? forms : sampleForms;

  return (
    <div>
      <Row className="mb-4">
        <Col>
          <h1>Forms and Instructions</h1>
        </Col>
        <Col xs="auto">
          <Button variant="primary">Upload New Form</Button>
        </Col>
      </Row>

      <Card>
        <Card.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Series Code</th>
                <th>Form Name</th>
                <th>Effective Date</th>
                <th>End Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {displayForms.map((form) => (
                <tr key={form.id}>
                  <td>{form.series_code}</td>
                  <td>{form.form_name || form.series_code + ' - Consolidated Financial Statements'}</td>
                  <td>{form.effective_date ? new Date(form.effective_date).toLocaleDateString() : 'N/A'}</td>
                  <td>{form.end_date ? new Date(form.end_date).toLocaleDateString() : 'Current'}</td>
                  <td>
                    <Button 
                      variant="primary" 
                      size="sm" 
                      className="me-2"
                      onClick={() => window.open(form.form_pdf_path, '_blank')}
                    >
                      Download Form
                    </Button>
                    <Button 
                      variant="info" 
                      size="sm"
                      onClick={() => window.open(form.instructions_pdf_path, '_blank')}
                    >
                      Download Instructions
                    </Button>
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

export default Forms;


