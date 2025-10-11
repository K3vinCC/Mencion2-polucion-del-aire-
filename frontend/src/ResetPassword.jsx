import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './login.css';

class AuthAdapter {
  constructor(baseURL = 'http://localhost:5000') { 
    this.baseURL = baseURL;
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

export default function ResetPassword() {
  const { token } = useParams();
  const navigate = useNavigate();
  
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [verifying, setVerifying] = useState(true);
  const [message, setMessage] = useState(null);
  const [tokenValid, setTokenValid] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [passwordChanged, setPasswordChanged] = useState(false);

  useEffect(() => {
    verifyToken();
  }, [token]);

  const verifyToken = async () => {
    const authAdapter = new AuthAdapter();
    const res = await authAdapter.verifyResetToken(token);
    
    setVerifying(false);
    
    if (res.success) {
      setTokenValid(true);
      setUserEmail(res.email);
    } else {
      setTokenValid(false);
      setMessage(res);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password.length < 6) {
      setMessage({ 
        success: false, 
        message: 'La contraseña debe tener al menos 6 caracteres' 
      });
      return;
    }

    if (password !== confirmPassword) {
      setMessage({ 
        success: false, 
        message: 'Las contraseñas no coinciden' 
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    const authAdapter = new AuthAdapter();
    const res = await authAdapter.resetPassword(token, password);

    setLoading(false);
    setMessage(res);

    if (res.success) {
      setPasswordChanged(true);
      setTimeout(() => {
        navigate('/');
      }, 3000);
    }
  };

  if (verifying) {
    return (
      <div className="auth-container">
        <div className="bg-gradient"></div>
        <div className="bg-pattern"></div>
        <div className="auth-content">
          <div className="auth-card">
            <div style={{ textAlign: 'center', padding: '40px 0' }}>
              <div className="spinner"></div>
              <p style={{ marginTop: '20px', color: '#64748b' }}>
                Verificando enlace...
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!tokenValid) {
    return (
      <div className="auth-container">
        <div className="bg-gradient"></div>
        <div className="bg-pattern"></div>
        <div className="auth-content">
          <div className="auth-card">
            <div className="auth-header">
              <div className="auth-avatar" style={{ color: '#ef4444' }}>
                <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                  <circle cx="32" cy="32" r="20" stroke="currentColor" strokeWidth="3"/>
                  <path d="M32 22v12m0 4h.01" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
                </svg>
              </div>
              <h2 className="auth-title">Enlace Inválido</h2>
              <p className="auth-subtitle">
                Este enlace ha expirado o no es válido
              </p>
            </div>

            <div className="auth-form">
              {message && (
                <div className="message error">
                  {message.message}
                </div>
              )}
              
              <button 
                className="auth-btn primary" 
                onClick={() => navigate('/forgot-password')}
              >
                <span>Solicitar Nuevo Enlace</span>
              </button>
            </div>

            <div className="auth-footer">
              <p>¿Tienes una cuenta?</p>
              <button 
                className="link-btn" 
                onClick={() => navigate('/')}
              >
                Iniciar sesión
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

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

      <div className="auth-content">
        <div className="auth-card">
          <div className="auth-header">
            <div className="auth-avatar">
              <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <circle cx="32" cy="32" r="20" stroke="currentColor" strokeWidth="3" opacity="0.8"/>
                <path d="M28 32l4 4 8-8" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h2 className="auth-title">Nueva Contraseña</h2>
            <p className="auth-subtitle">
              {passwordChanged 
                ? '¡Contraseña actualizada!' 
                : `Establecer nueva contraseña para ${userEmail}`}
            </p>
          </div>

          <div className="auth-form">
            {!passwordChanged ? (
              <>
                <div className="form-group">
                  <label>Nueva Contraseña</label>
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
                      minLength="6"
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
                      minLength="6"
                    />
                  </div>
                </div>

                <button 
                  className="auth-btn primary" 
                  onClick={handleSubmit} 
                  disabled={loading}
                >
                  {loading ? (
                    <div className="spinner"></div>
                  ) : (
                    <>
                      <span>Restablecer Contraseña</span>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M5 12h14m-7-7 7 7-7 7" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </>
                  )}
                </button>
              </>
            ) : (
              <div style={{ textAlign: 'center', padding: '20px 0' }}>
                <div style={{ fontSize: '48px', marginBottom: '20px' }}>✅</div>
                <p style={{ marginBottom: '10px', color: '#64748b' }}>
                  Tu contraseña ha sido actualizada exitosamente.
                </p>
                <p style={{ fontSize: '14px', color: '#94a3b8' }}>
                  Serás redirigido al inicio de sesión en unos segundos...
                </p>
              </div>
            )}

            {message && (
              <div className={`message ${message.success ? 'success' : 'error'}`}>
                {message.message}
              </div>
            )}
          </div>

          {!passwordChanged && (
            <div className="auth-footer">
              <p>¿Recordaste tu contraseña?</p>
              <button 
                className="link-btn" 
                onClick={() => navigate('/')}
              >
                Volver al inicio de sesión
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}