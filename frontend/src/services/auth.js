class AuthAdapter {
  constructor(baseURL = 'http://localhost:5000/auth') { // <-- incluye /auth
    this.baseURL = baseURL;
  }

  async authenticate({ email, password }) {
    try {
      const res = await fetch(`${this.baseURL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  async register({ nombre, email, password, role }) {
    try {
      const url = role === 'conserje'
        ? `${this.baseURL}/register/conserje`
        : `${this.baseURL}/register`;

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre_completo: nombre, // Flask espera este campo
          email,
          password,
          rol: role
        })
      });

      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }
}
