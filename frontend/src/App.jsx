import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import ModernAuthSystem from "./login";
import PrivateRoute from "./services/PrivateRoute";
import Principal from "./Principal";
import AdminPage from "./pages/AdminPage";
import ConserjePage from "./pages/ConserjePage";


function App() {
  return (
    <Router> {}
      <Routes>
        {}
        <Route path="/" element={<ModernAuthSystem />} />

        {}
        <Route element={<PrivateRoute />}>
          <Route path="/principal" element={<Principal />} />
        </Route>

        <Route element={<PrivateRoute requiredRole="admin" />}>
          <Route path="/principal" element={<Principal />} />
        </Route>

        <Route element={<PrivateRoute requiredRole="conserje" />}>
          <Route path="/principal" element={<Principal />} />
        </Route>

        {}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;