import React, { useState } from 'react';
import './login.css';

function LoginModel({ email = '', password = '', role = 'admin' } = {}) {
  return { email, password, role };
}

class AuthAdapter {
  async authenticate({ email, password, role }) {
    await new Promise(r => setTimeout(r, 500));
    if (!email || !password) return { success: false, message: 'Faltan credenciales' };
    if (password.length < 6) return { success: false, message: 'Contraseña muy corta' };
    return { success: true, message: `Autenticado como ${role}` };
  }
}

class LoginUseCase {
  constructor(authAdapter) {
    this.authAdapter = authAdapter;
  }

  async execute(model) {
    if (!model.email.includes('@')) return { success: false, message: 'Email inválido' };
    return await this.authAdapter.authenticate(model);
  }
}

class LoginController {
  constructor(loginUseCase) {
    this.loginUseCase = loginUseCase;
  }

  async login({ email, password, role, onResult }) {
    const model = LoginModel({ email, password, role });
    const res = await this.loginUseCase.execute(model);
    if (typeof onResult === 'function') onResult(res);
    return res;
  }
}

export default function LoginHexagonal() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('admin');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const authAdapter = new AuthAdapter();
  const loginUseCase = new LoginUseCase(authAdapter);
  const controller = new LoginController(loginUseCase);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    const res = await controller.login({
      email,
      password,
      role,
      onResult: (r) => setMessage(r.message),
    });
    setLoading(false);
    if (res.success) console.log('Redirect to dashboard...');
  };

  return (
    <div className="lh-root">
      <div className="lh-logo">
        <img src="/logo.png" alt="Logo" />
      </div>

      <div className="lh-card">
        <div className="lh-avatar">
          <svg
            width="84"
            height="96"
            viewBox="0 0 72 84"
            fill="none"
          >
            <ellipse cx="36" cy="27" rx="20" ry="18" fill="#111827" />
            <path d="M10 68c0-12 14-24 26-24s26 12 26 24H10z" fill="#111827" />
          </svg>
        </div>

        <div className="lh-roles">
          <label className="lh-role">
            Administrador
            <input
              type="radio"
              name="role"
              checked={role === 'admin'}
              onChange={() => setRole('admin')}
            />
            <span className="lh-dot filled" />
          </label>

          <label className="lh-role">
            Conserje
            <input
              type="radio"
              name="role"
              checked={role === 'conserje'}
              onChange={() => setRole('conserje')}
            />
            <span className="lh-dot" />
          </label>
        </div>

        <form className="lh-form" onSubmit={handleSubmit}>
          <div className="lh-field">
            <label>Correo Electronico</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="usuario@ejemplo.com"
            />
          </div>

          <div className="lh-field">
            <label>Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="********"
            />
          </div>

          <div className="lh-buttons">
            <button className="lh-btn" type="submit" disabled={loading}>
              Iniciar Sesión
            </button>
          </div>

          {message && <div className="lh-message">{message}</div>}
        </form>
      </div>
    </div>
  );
}
