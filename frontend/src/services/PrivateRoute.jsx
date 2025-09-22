import React from "react";
import { Navigate, Outlet } from "react-router-dom";

const PrivateRoute = ({ requiredRole }) => {
  const user = JSON.parse(localStorage.getItem("user"));
  console.log('PrivateRoute user:', user, 'requiredRole:', requiredRole);

  if (!user || (requiredRole && user.rol !== requiredRole)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
};


export default PrivateRoute;
