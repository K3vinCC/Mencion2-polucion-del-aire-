import React from "react";
import { useNavigate } from "react-router-dom"; // Importa useNavigate

// Define la función de logout en el mismo archivo
const logout = (navigate) => {
  localStorage.removeItem("user");
  navigate("/");
};

function PrincipalPage() {
  const navigate = useNavigate(); // Hook para la navegación

  return (
    <div>
      <h1>Bienvenido a la página principal</h1>
      <p>Has iniciado sesión correctamente.</p>
      {/* Agrega un botón que al hacer clic llame a la función de logout */}
      <button onClick={() => logout(navigate)}>Cerrar Sesión</button>
    </div>
  );
}

export default PrincipalPage;