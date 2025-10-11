import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import ModernAuthSystem from './login.jsx';
import Principal from './Principal.jsx';
import PrincipalC from './PrincipalC.jsx';
import ForgotPassword from './ForgotPassword';
import ResetPassword from './ResetPassword';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ModernAuthSystem />} />
        <Route path="/principalC" element={<PrincipalC />} />
        <Route path="/principal" element={<Principal />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />
        
      </Routes>
    </BrowserRouter>
  </StrictMode>
);