



import React, { useState, useEffect } from 'react';
import { Table, Button, Card, Row, Col, Spinner, Alert, Badge, Form, Modal } from 'react-bootstrap';
import axios from 'axios';

const ValidationRules = () => {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [ruleTypes] = useState([
    'data_type', 'range', 'format', 'cross_field', 'historical', 'mathematical'
  ]);

  useEffect(() => {
    const fetchRules = async () => {
      try {
        const response = await axios.get('/validation/rules');
        setRules(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching validation rules:', err);
        setError('Failed to load validation rules. Please try again later.');
        setLoading(false);
      }
    };

    fetchRules();
  }, []);

  const handleCloseModal = () => setShowModal(false);
  const handleShowModal = () => setShowModal(true);

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

  // Sample rules data if API doesn't return any
  const sampleRules = [
    {
      id: 1,
      rule_name: 'Total Assets Validation',
      rule_description: 'Validates that total assets equals sum of individual asset categories',
      rule_type: 'mathematical',
      severity: 'error',
      effective_date: '2024-01-01',
      end_date: null,
      status: 'active'
    },
    {
      id: 2,
      rule_name: 'Loan Amount Range Check',
      rule_description: 'Validates that loan amounts are within acceptable ranges',
      rule_type: 'range',
      severity: 'warning',
      effective_date: '2024-01-01',
      end_date: null,
      status: 'active'
    },
    {
      id: 3,
      rule_name: 'Date Format Validation',
      rule_description: 'Validates that dates are in the correct format',
      rule_type: 'format',
      severity: 'error',
      effective_date: '2024-01-01',
      end_date: null,
      status: 'active'
    }
  ];

  const displayRules = rules.length > 0 ? rules : sampleRules;

  return (
    <div>
      <Row className="mb-4">
        <Col>
          <h1>Validation Rules</h1>
        </Col>
        <Col xs="auto">
          <Button variant="primary" onClick={handleShowModal}>Add New Rule</Button>
        </Col>
      </Row>

      <Card>
        <Card.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>ID</th>
                <th>Rule Name</th>
                <th>Description</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Effective Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {displayRules.map((rule) => (
                <tr key={rule.id}>
                  <td>{rule.id}</td>
                  <td>{rule.rule_name}</td>
                  <td>{rule.rule_description}</td>
                  <td>{rule.rule_type}</td>
                  <td>
                    <Badge bg={rule.severity === 'error' ? 'danger' : 'warning'}>
                      {rule.severity}
                    </Badge>
                  </td>
                  <td>{new Date(rule.effective_date).toLocaleDateString()}</td>
                  <td>
                    <Badge bg={rule.status === 'active' ? 'success' : 'secondary'}>
                      {rule.status}
                    </Badge>
                  </td>
                  <td>
                    <Button variant="info" size="sm" className="me-2">View</Button>
                    <Button variant="warning" size="sm" className="me-2">Edit</Button>
                    <Button variant="danger" size="sm">Delete</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Add New Rule Modal */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Add New Validation Rule</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Rule Name</Form.Label>
              <Form.Control type="text" placeholder="Enter rule name" />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control as="textarea" rows={3} placeholder="Enter rule description" />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Rule Type</Form.Label>
              <Form.Select>
                <option value="">Select rule type</option>
                {ruleTypes.map(type => (
                  <option key={type} value={type}>
                    {type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Rule Definition</Form.Label>
              <Form.Control as="textarea" rows={5} placeholder="Enter rule definition (JSON or expression)" />
              <Form.Text className="text-muted">
                Define the rule using JSON format or a mathematical expression.
              </Form.Text>
            </Form.Group>

            <Row className="mb-3">
              <Col>
                <Form.Group>
                  <Form.Label>Severity</Form.Label>
                  <Form.Select>
                    <option value="error">Error</option>
                    <option value="warning">Warning</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group>
                  <Form.Label>Effective Date</Form.Label>
                  <Form.Control type="date" />
                </Form.Group>
              </Col>
            </Row>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleCloseModal}>
            Save Rule
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default ValidationRules;



