class AuthAdapter {
  constructor(baseURL = 'http://localhost:5000') { 
    this.baseURL = baseURL;
  }

  async authenticate({ email, password }) {
    try {
      const res = await fetch(`${this.baseURL}/auth/login`, {
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
      const res = await fetch(`${this.baseURL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre_completo: nombre,
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
  async forgotPassword(email) {
    try {
      const res = await fetch(`${this.baseURL}/auth/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  async verifyResetToken(token) {
    try {
      const res = await fetch(`${this.baseURL}/auth/verify-reset-token/${token}`);
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  async resetPassword(token, password) {
    try {
      const res = await fetch(`${this.baseURL}/auth/reset-password/${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }
}
