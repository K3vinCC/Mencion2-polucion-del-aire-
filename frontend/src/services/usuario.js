class UsuarioAdapter {
  constructor(baseURL = 'http://localhost:5000/usuario') {
    this.baseURL = baseURL;
  }

  // Listar todos los usuarios
  async listar() {
    try {
      const res = await fetch(`${this.baseURL}/listar`);
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  // Crear usuario (puedes usar register de AuthAdapter en vez de este)
  async crear({ nombre, email, password, rol }) {
    try {
      const res = await fetch(`${this.baseURL}/crear`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre_completo: nombre,
          email,
          password,
          rol
        })
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  // Actualizar usuario
  async actualizar(id, { nombre, email, rol }) {
    try {
      const res = await fetch(`${this.baseURL}/${id}/actualizar`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre_completo: nombre,
          email,
          rol
        })
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  // Eliminar usuario
  async eliminar(id) {
    try {
      const res = await fetch(`${this.baseURL}/${id}/eliminar`, {
        method: 'DELETE'
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }
}

export default UsuarioAdapter;
