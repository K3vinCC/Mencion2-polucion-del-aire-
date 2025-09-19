import React, { useState } from 'react';
import './login.css';
function LoginModel({ email = '', password = '', role = 'admin' } = {}) {
  return { email, password, role };
}

function RegisterModel({ name = '', email = '', password = '', confirmPassword = '', role = 'admin' } = {}) {
  return { name, email, password, confirmPassword, role };
}

class AuthAdapter {
  async authenticate({ email, password, role }) {
    await new Promise(r => setTimeout(r, 800));
    if (!email || !password) return { success: false, message: 'Faltan credenciales' };
    if (password.length < 6) return { success: false, message: 'Contraseña muy corta' };
    return { success: true, message: `Autenticado como ${role}` };
  }

  async register({ name, email, password, confirmPassword, role }) {
    await new Promise(r => setTimeout(r, 1000));
    if (!name || !email || !password || !confirmPassword) {
      return { success: false, message: 'Todos los campos son requeridos' };
    }
    if (password !== confirmPassword) {
      return { success: false, message: 'Las contraseñas no coinciden' };
    }
    if (password.length < 6) {
      return { success: false, message: 'Contraseña debe tener al menos 6 caracteres' };
    }
    return { success: true, message: `Usuario ${name} registrado como ${role}` };
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

class RegisterUseCase {
  constructor(authAdapter) {
    this.authAdapter = authAdapter;
  }

  async execute(model) {
    if (!model.email.includes('@')) return { success: false, message: 'Email inválido' };
    return await this.authAdapter.register(model);
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

class RegisterController {
  constructor(registerUseCase) {
    this.registerUseCase = registerUseCase;
  }

  async register({ name, email, password, confirmPassword, role, onResult }) {
    const model = RegisterModel({ name, email, password, confirmPassword, role });
    const res = await this.registerUseCase.execute(model);
    if (typeof onResult === 'function') onResult(res);
    return res;
  }
}

function LoginForm({ onSwitchToRegister }) {
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
      onResult: (r) => setMessage(r),
    });
    setLoading(false);
    if (res.success) console.log('Redirect to dashboard...');
  };

  return (
    <div className="auth-card">
      <div className="auth-header">
        <div className="auth-avatar">
          <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
            <circle cx="32" cy="20" r="12" fill="currentColor" opacity="0.8"/>
            <path d="M12 52c0-8 9-16 20-16s20 8 20 16H12z" fill="currentColor" opacity="0.8"/>
          </svg>
        </div>
        <h2 className="auth-title">Iniciar Sesión</h2>
        <p className="auth-subtitle">Bienvenido de vuelta</p>
      </div>

      <div className="role-selector">
        <div className={`role-option ${role === 'admin' ? 'active' : ''}`} 
             onClick={() => setRole('admin')}>
          <div className="role-icon">👨‍💼</div>
          <span>Administrador</span>
        </div>
        <div className={`role-option ${role === 'conserje' ? 'active' : ''}`} 
             onClick={() => setRole('conserje')}>
          <div className="role-icon">🔧</div>
          <span>Conserje</span>
        </div>
      </div>

      <div className="auth-form">
        <div className="form-group">
          <label>Correo Electrónico</label>
          <div className="input-wrapper">
            <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" strokeWidth="2"/>
              <polyline points="22,6 12,13 2,6" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="usuario@ejemplo.com"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label>Contraseña</label>
          <div className="input-wrapper">
            <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
              <circle cx="12" cy="16" r="1" fill="currentColor"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
        </div>

        <button className="auth-btn primary" onClick={handleSubmit} disabled={loading}>
          {loading ? (
            <div className="spinner"></div>
          ) : (
            <>
              <span>Iniciar Sesión</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14m-7-7 7 7-7 7" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </>
          )}
        </button>

        {message && (
          <div className={`message ${message.success ? 'success' : 'error'}`}>
            {message.message}
          </div>
        )}
      </div>

      <div className="auth-footer">
        <p>¿No tienes una cuenta?</p>
        <button className="link-btn" onClick={onSwitchToRegister}>
          Crear cuenta
        </button>
      </div>
    </div>
  );
}

function RegisterForm({ onSwitchToLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('admin');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const authAdapter = new AuthAdapter();
  const registerUseCase = new RegisterUseCase(authAdapter);
  const controller = new RegisterController(registerUseCase);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    const res = await controller.register({
      name,
      email,
      password,
      confirmPassword,
      role,
      onResult: (r) => setMessage(r),
    });
    setLoading(false);
    if (res.success) {
      setTimeout(() => onSwitchToLogin(), 2000);
    }
  };

  return (
    <div className="auth-card">
      <div className="auth-header">
        <div className="auth-avatar register">
          <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
            <circle cx="32" cy="20" r="12" fill="currentColor" opacity="0.8"/>
            <path d="M12 52c0-8 9-16 20-16s20 8 20 16H12z" fill="currentColor" opacity="0.8"/>
            <circle cx="48" cy="16" r="8" fill="#10b981"/>
            <path d="M44 16l2 2 4-4" stroke="white" strokeWidth="2" fill="none"/>
          </svg>
        </div>
        <h2 className="auth-title">Crear Cuenta</h2>
        <p className="auth-subtitle">Únete a nosotros</p>
      </div>

      <div className="role-selector">
        <div className={`role-option ${role === 'admin' ? 'active' : ''}`} 
             onClick={() => setRole('admin')}>
          <div className="role-icon">👨‍💼</div>
          <span>Administrador</span>
        </div>
        <div className={`role-option ${role === 'conserje' ? 'active' : ''}`} 
             onClick={() => setRole('conserje')}>
          <div className="role-icon">🔧</div>
          <span>Conserje</span>
        </div>
      </div>

      <div className="auth-form">
        <div className="form-group">
          <label>Nombre Completo</label>
          <div className="input-wrapper">
            <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2"/>
              <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Juan Pérez"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label>Correo Electrónico</label>
          <div className="input-wrapper">
            <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" strokeWidth="2"/>
              <polyline points="22,6 12,13 2,6" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="usuario@ejemplo.com"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label>Contraseña</label>
          <div className="input-wrapper">
            <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
              <circle cx="12" cy="16" r="1" fill="currentColor"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label>Confirmar Contraseña</label>
          <div className="input-wrapper">
            <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
              <circle cx="12" cy="16" r="1" fill="currentColor"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
        </div>

        <button className="auth-btn primary" onClick={handleSubmit} disabled={loading}>
          {loading ? (
            <div className="spinner"></div>
          ) : (
            <>
              <span>Crear Cuenta</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14m-7-7 7 7-7 7" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </>
          )}
        </button>

        {message && (
          <div className={`message ${message.success ? 'success' : 'error'}`}>
            {message.message}
          </div>
        )}
      </div>

      <div className="auth-footer">
        <p>¿Ya tienes una cuenta?</p>
        <button className="link-btn" onClick={onSwitchToLogin}>
          Iniciar sesión
        </button>
      </div>
    </div>
  );
}

export default function ModernAuthSystem() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="auth-container">
      <div className="bg-gradient"></div>
      <div className="bg-pattern"></div>
      <div className="floating-elements">
        <div className="floating-circle" style={{ top: '10%', left: '10%' }}></div>
        <div className="floating-circle" style={{ top: '70%', right: '15%' }}></div>
        <div className="floating-triangle" style={{ top: '30%', right: '10%' }}></div>
        <div className="floating-square" style={{ bottom: '20%', left: '15%' }}></div>
      </div>

      <div className="logo-container">
        <div className="logo">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
            <circle cx="20" cy="20" r="20" fill="url(#gradient)"/>
            <path d="M15 20l5 5 10-10" stroke="white" strokeWidth="2" fill="none"/>
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#ffffffff"/>
                <stop offset="100%" stopColor="#ffffffff"/>
              </linearGradient>
            </defs>
          </svg>
          <span>Universidad Catolica de Temuco</span>
        </div>
      </div>

      <div className="auth-content">
        {isLogin ? (
          <LoginForm onSwitchToRegister={() => setIsLogin(false)} />
        ) : (
          <RegisterForm onSwitchToLogin={() => setIsLogin(true)} />
        )}
      </div>
    </div>
  );
}