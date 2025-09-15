














































import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-light py-3 mt-auto">
      <Container className="text-center">
        <p className="mb-0 text-muted">
          &copy; {currentYear} Federal Reserve Data Collection System
        </p>
      </Container>
    </footer>
  );
};

export default Footer;














































