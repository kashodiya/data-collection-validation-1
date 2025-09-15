












import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Institutions from './pages/Institutions';
import InstitutionDetail from './pages/InstitutionDetail';
import ReportSeries from './pages/ReportSeries';
import Submissions from './pages/Submissions';
import Forms from './pages/Forms';
import ValidationRules from './pages/ValidationRules';
import MDRMDictionary from './pages/MDRMDictionary';
import Users from './pages/Users';
import Profile from './pages/Profile';

// Context
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';

// Styles
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App d-flex flex-column min-vh-100">
          <Header />
          <Container className="flex-grow-1 py-4">
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              
              {/* Private Routes */}
              <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
              <Route path="/institutions" element={<PrivateRoute><Institutions /></PrivateRoute>} />
              <Route path="/institutions/:id" element={<PrivateRoute><InstitutionDetail /></PrivateRoute>} />
              <Route path="/report-series" element={<PrivateRoute><ReportSeries /></PrivateRoute>} />
              <Route path="/submissions" element={<PrivateRoute><Submissions /></PrivateRoute>} />
              <Route path="/forms" element={<PrivateRoute><Forms /></PrivateRoute>} />
              <Route path="/validation/rules" element={<PrivateRoute><ValidationRules /></PrivateRoute>} />
              <Route path="/mdrm/dictionary" element={<PrivateRoute><MDRMDictionary /></PrivateRoute>} />
              <Route path="/users" element={<PrivateRoute><Users /></PrivateRoute>} />
              <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
              
              {/* Redirect to Dashboard */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Container>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;












