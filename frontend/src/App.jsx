import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import ModernAuthSystem from "./login";
import PrivateRoute from "./services/PrivateRoute";
import Principal from "./Principal";
import PrincipalC from "./PrincipalC";
import AdminPage from "./pages/AdminPage";
import ConserjePage from "./pages/ConserjePage";
import ForgotPassword from './ForgotPassword';
import ResetPassword from './ResetPassword';


function App() {
  return (
    <Router> {}
      <Routes>
        {}
        <Route path="/" element={<ModernAuthSystem />} />

        {}
        <Route element={<PrivateRoute />}>
          <Route path="/principal" element={<PrincipalC />} />
        </Route>

        <Route element={<PrivateRoute requiredRole="admin" />}>
          <Route path="/principal" element={<Principal />} />
        </Route>

        <Route element={<PrivateRoute requiredRole="conserje" />}>
          <Route path="/principalC" element={<PrincipalC />} />
        </Route>
        <Route path="/forgot-password" element={<ForgotPassword />} />
        
        <Route path="/reset-password/:token" element={<ResetPassword />} />
        

        {}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;