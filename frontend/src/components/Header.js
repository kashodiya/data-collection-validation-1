




































import React, { useContext } from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Header = () => {
  const { currentUser, logout, hasRole } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Navbar bg="primary" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Federal Reserve Data Collection</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {currentUser && (
              <>
                <Nav.Link as={Link} to="/">Dashboard</Nav.Link>
                
                {/* Institutions - All users can view */}
                <Nav.Link as={Link} to="/institutions">Institutions</Nav.Link>
                
                {/* Report Series - All users can view */}
                <Nav.Link as={Link} to="/report-series">Report Series</Nav.Link>
                
                {/* Submissions - All users can view */}
                <Nav.Link as={Link} to="/submissions">Submissions</Nav.Link>
                
                {/* Forms - All users can view */}
                <Nav.Link as={Link} to="/forms">Forms</Nav.Link>
                
                {/* Validation Rules - Only analysts and admins can view */}
                {hasRole('analyst') && (
                  <>
                    <Nav.Link as={Link} to="/validation/rules">Validation Rules</Nav.Link>
                    <Nav.Link as={Link} to="/mdrm/dictionary">MDRM Dictionary</Nav.Link>
                  </>
                )}
                
                {/* User Management - Only admins can view */}
                {hasRole('admin') && (
                  <Nav.Link as={Link} to="/users">Users</Nav.Link>
                )}
              </>
            )}
          </Nav>
          
          <Nav>
            {currentUser ? (
              <NavDropdown title={currentUser.username} id="basic-nav-dropdown" align="end">
                <NavDropdown.Item as={Link} to="/profile">Profile</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={handleLogout}>Logout</NavDropdown.Item>
              </NavDropdown>
            ) : (
              <Nav.Link as={Link} to="/login">Login</Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;




































