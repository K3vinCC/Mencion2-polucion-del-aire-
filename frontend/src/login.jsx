import React, { useState } from 'react';
import './login.css';
import logoImg from './assets/logouct.png';
import { useNavigate } from 'react-router-dom';
function LoginModel({ email = '', password = '', role = 'admin' } = {}) {
  return { email, password, role };
}

function RegisterModel({ name = '', email = '', password = '', confirmPassword = '', role = 'admin' } = {}) {
  return { name, email, password, confirmPassword, role };
}

class AuthAdapter {
  constructor(baseURL = 'http://localhost:5000') { // Solo host
    this.baseURL = baseURL;
  }

  async authenticate({ email, password }) {
    const res = await fetch(`${this.baseURL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    return await res.json();
  }

  async register({ nombre, email, password, role }) {
    const url = role === "conserje" ? `${this.baseURL}/auth/register/conserje` : `${this.baseURL}/auth/register`;
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre_completo: nombre, email, password, rol: role })
    });
    return await res.json();
  }
}



class LoginUseCase {
  constructor(authAdapter) { 
    this.authAdapter = authAdapter; 
  }

  async execute(model) {
    if (!model.email.includes('@')) 
      return { success: false, message: 'Email inválido' };

    const res = await this.authAdapter.authenticate(model);

    if (!res.success) return res; // credenciales inválidas

    // Mapear rol_id del backend a nombre
    const backendRol = res.rol === 1 ? 'admin' : 'conserje';

    if (backendRol !== model.role) {
      return { success: false, message: 'Credenciales inválidas' };
    }

    // ✅ Login correcto → guardar info en localStorage
    localStorage.setItem("user", JSON.stringify({
      email: model.email,
      rol: backendRol,
      token: res.token || "fake-jwt"
    }));

    return { success: true, message: 'Login exitoso', rol: backendRol };
  }
}



class RegisterUseCase {
  constructor(authAdapter) { this.authAdapter = authAdapter; }

  async execute({ nombre, email, password, confirmPassword, role }) {
    if (password !== confirmPassword) {
      return { success: false, message: 'Las contraseñas no coinciden' };
    }
    return await this.authAdapter.register({ nombre, email, password, role });
  }
}

class LoginController {
  constructor(loginUseCase) { this.loginUseCase = loginUseCase; }

  async login({ email, password, role, onResult }) {
    const res = await this.loginUseCase.execute({ email, password, role });
    if (onResult) onResult(res);
    return res;
  }
}

class RegisterController {
  constructor(registerUseCase) { this.registerUseCase = registerUseCase; }

  async register({ nombre, email, password, confirmPassword, role, onResult }) {
    const res = await this.registerUseCase.execute({ nombre, email, password, confirmPassword, role });
    if (onResult) onResult(res);
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
  const navigate = useNavigate(); // <-- agregar

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

    if (res.success) {
      // Usa un switch o if-else para navegar según el rol devuelto por el caso de uso
      switch(res.rol) {
        case 'admin':
          navigate('/principal');
          break;
        case 'conserje':
          navigate('/principal');
          break;
        default:
          navigate('/principal'); // Alternativa para otros roles o acceso general
          break;
      }
    }
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
  const navigate = useNavigate(); 
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    const res = await controller.register({
      nombre: name,
      email,
      password,
      confirmPassword,
      role,
      onResult: (r) => setMessage(r)
    });

    setLoading(false);

    if (res.success) {
      // Mapear rol correctamente
      const backendRol = role; // el rol que seleccionaste al registrar
      localStorage.setItem("user", JSON.stringify({
        email,
        rol: backendRol,
        token: res.token || "fake-jwt"
      }));
      navigate('/principal');
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
          <img src={logoImg} alt="Logo" style={{ height: '60px', marginRight: '0.5rem' }} />
          <span>Universidad Catolica de Temuco</span>
        </div>
      </div>
      <span className='nombreweb'>EcoAula UCT</span> 
      <span className='nombrewebsecundario'>"Cuidando el aula, potenciando el rendimiento estudiantil."</span>
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