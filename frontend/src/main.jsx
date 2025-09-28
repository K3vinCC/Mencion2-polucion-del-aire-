import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import ModernAuthSystem from './login.jsx';
import Principal from './Principal.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ModernAuthSystem />} />
        <Route path="/principal" element={<Principal />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);