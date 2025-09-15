































import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Spinner } from 'react-bootstrap';

const PrivateRoute = ({ children, requiredRole }) => {
  const { currentUser, loading, hasRole } = useContext(AuthContext);

  // Show loading spinner while checking authentication
  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '80vh' }}>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  // If not authenticated, redirect to login
  if (!currentUser) {
    return <Navigate to="/login" />;
  }

  // If requiredRole is specified, check if user has the required role
  if (requiredRole && !hasRole(requiredRole)) {
    // User doesn't have the required role, redirect to dashboard
    return <Navigate to="/" />;
  }

  // User is authenticated and has the required role (if specified)
  return children;
};

export default PrivateRoute;































