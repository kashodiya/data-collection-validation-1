




import React, { useState, useEffect } from 'react';
import { Table, Button, Card, Row, Col, Spinner, Alert, Form, InputGroup } from 'react-bootstrap';
import axios from 'axios';

const MDRMDictionary = () => {
  const [mdrmItems, setMdrmItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredItems, setFilteredItems] = useState([]);

  useEffect(() => {
    const fetchMDRMItems = async () => {
      try {
        const response = await axios.get('/mdrm/items');
        setMdrmItems(response.data);
        setFilteredItems(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching MDRM items:', err);
        setError('Failed to load MDRM dictionary. Please try again later.');
        setLoading(false);
      }
    };

    fetchMDRMItems();
  }, []);

  useEffect(() => {
    if (searchTerm) {
      const filtered = mdrmItems.filter(item => 
        item.mdrm_identifier.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.item_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.series_mnemonic.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredItems(filtered);
    } else {
      setFilteredItems(mdrmItems);
    }
  }, [searchTerm, mdrmItems]);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleImportDictionary = () => {
    // This would trigger a file upload dialog and then send the file to the backend
    alert('Import dictionary functionality would be implemented here');
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

  // Sample MDRM items if API doesn't return any
  const sampleMDRMItems = [
    {
      id: 1,
      mdrm_identifier: 'BHCK2170',
      item_name: 'Total Assets',
      item_definition: 'The sum of all assets owned by the reporting entity as of the report date.',
      data_type: 'NUMERIC',
      valid_values: '>= 0',
      series_mnemonic: 'FR Y-9C',
      effective_date: '2020-01-01',
      end_date: null
    },
    {
      id: 2,
      mdrm_identifier: 'BHCK2948',
      item_name: 'Total Liabilities',
      item_definition: 'The sum of all liabilities owed by the reporting entity as of the report date.',
      data_type: 'NUMERIC',
      valid_values: '>= 0',
      series_mnemonic: 'FR Y-9C',
      effective_date: '2020-01-01',
      end_date: null
    },
    {
      id: 3,
      mdrm_identifier: 'BHCK3210',
      item_name: 'Total Equity Capital',
      item_definition: 'The total equity capital of the reporting entity as of the report date.',
      data_type: 'NUMERIC',
      valid_values: 'Any',
      series_mnemonic: 'FR Y-9C',
      effective_date: '2020-01-01',
      end_date: null
    },
    {
      id: 4,
      mdrm_identifier: 'RCON2170',
      item_name: 'Total Assets',
      item_definition: 'The sum of all assets owned by the reporting entity as of the report date.',
      data_type: 'NUMERIC',
      valid_values: '>= 0',
      series_mnemonic: 'FFIEC 031',
      effective_date: '2020-01-01',
      end_date: null
    }
  ];

  const displayItems = filteredItems.length > 0 ? filteredItems : sampleMDRMItems;

  return (
    <div>
      <Row className="mb-4">
        <Col>
          <h1>MDRM Data Dictionary</h1>
        </Col>
        <Col xs="auto">
          <Button variant="primary" onClick={handleImportDictionary}>Import Dictionary</Button>
        </Col>
      </Row>

      <Card className="mb-4">
        <Card.Body>
          <Form>
            <InputGroup>
              <Form.Control
                placeholder="Search by MDRM ID, Item Name, or Series..."
                value={searchTerm}
                onChange={handleSearch}
              />
              <Button variant="outline-secondary">
                Search
              </Button>
            </InputGroup>
          </Form>
        </Card.Body>
      </Card>

      <Card>
        <Card.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>MDRM ID</th>
                <th>Item Name</th>
                <th>Data Type</th>
                <th>Valid Values</th>
                <th>Series</th>
                <th>Effective Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {displayItems.map((item) => (
                <tr key={item.id}>
                  <td>{item.mdrm_identifier}</td>
                  <td>{item.item_name}</td>
                  <td>{item.data_type}</td>
                  <td>{item.valid_values}</td>
                  <td>{item.series_mnemonic}</td>
                  <td>{new Date(item.effective_date).toLocaleDateString()}</td>
                  <td>
                    <Button variant="info" size="sm" className="me-2">View Details</Button>
                    <Button variant="warning" size="sm">Edit</Button>
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

export default MDRMDictionary;




