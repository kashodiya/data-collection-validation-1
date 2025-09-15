







import React, { useState, useContext, useEffect } from 'react';
import { Card, Form, Button, Alert, Row, Col } from 'react-bootstrap';
import { AuthContext } from '../context/AuthContext';
import axios from 'axios';

const Profile = () => {
  const { currentUser, updateCurrentUser } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [message, setMessage] = useState({ type: '', text: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentUser) {
      setFormData({
        username: currentUser.username || '',
        email: currentUser.email || '',
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    }
  }, [currentUser]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    // Validate passwords if user is trying to change password
    if (formData.newPassword) {
      if (!formData.currentPassword) {
        setMessage({ type: 'danger', text: 'Current password is required to set a new password' });
        setLoading(false);
        return;
      }
      
      if (formData.newPassword !== formData.confirmPassword) {
        setMessage({ type: 'danger', text: 'New passwords do not match' });
        setLoading(false);
        return;
      }
    }

    try {
      // Prepare update data
      const updateData = {
        email: formData.email
      };

      // Only include password fields if user is changing password
      if (formData.newPassword) {
        updateData.current_password = formData.currentPassword;
        updateData.new_password = formData.newPassword;
      }

      // Send update request
      const response = await axios.put(`/users/me`, updateData);
      
      // Update local user data
      updateCurrentUser({
        ...currentUser,
        email: formData.email
      });
      
      setMessage({ type: 'success', text: 'Profile updated successfully' });
      
      // Clear password fields
      setFormData({
        ...formData,
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    } catch (error) {
      console.error('Error updating profile:', error);
      setMessage({ 
        type: 'danger', 
        text: error.response?.data?.detail || 'Failed to update profile. Please try again.' 
      });
    } finally {
      setLoading(false);
    }
  };

  if (!currentUser) {
    return <Alert variant="warning">Please log in to view your profile.</Alert>;
  }

  return (
    <div>
      <h1 className="mb-4">My Profile</h1>
      
      <Card>
        <Card.Body>
          {message.text && (
            <Alert variant={message.type} dismissible onClose={() => setMessage({ type: '', text: '' })}>
              {message.text}
            </Alert>
          )}
          
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    name="username"
                    value={formData.username}
                    disabled
                  />
                  <Form.Text className="text-muted">
                    Username cannot be changed
                  </Form.Text>
                </Form.Group>
              </Col>
              
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            
            <h4 className="mt-4 mb-3">Change Password</h4>
            
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Current Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="currentPassword"
                    value={formData.currentPassword}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            </Row>
            
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>New Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="newPassword"
                    value={formData.newPassword}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
              
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Confirm New Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            </Row>
            
            <div className="d-flex justify-content-end mt-4">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? 'Updating...' : 'Update Profile'}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
      
      <Card className="mt-4">
        <Card.Body>
          <h4>Account Information</h4>
          <p><strong>Role:</strong> {currentUser.role}</p>
          <p><strong>Last Login:</strong> {currentUser.last_login ? new Date(currentUser.last_login).toLocaleString() : 'Never'}</p>
          {currentUser.institution_id && (
            <p><strong>Institution ID:</strong> {currentUser.institution_id}</p>
          )}
        </Card.Body>
      </Card>
    </div>
  );
};

export default Profile;







