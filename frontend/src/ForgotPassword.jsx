import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';

class AuthAdapter {
  constructor(baseURL = 'http://localhost:5000') { 
    this.baseURL = baseURL;
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
}

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [emailSent, setEmailSent] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email || !email.includes('@')) {
      setMessage({ success: false, message: 'Por favor ingresa un correo válido' });
      return;
    }

    setLoading(true);
    setMessage(null);

    const authAdapter = new AuthAdapter();
    const res = await authAdapter.forgotPassword(email);

    setLoading(false);
    setMessage(res);

    if (res.success) {
      setEmailSent(true);
    }
  };

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
                <path d="M32 22v12m0 4h.01" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
              </svg>
            </div>
            <h2 className="auth-title">Recuperar Contraseña</h2>
            <p className="auth-subtitle">
              {emailSent 
                ? '¡Revisa tu correo!' 
                : 'Ingresa tu correo electrónico'}
            </p>
          </div>

          <div className="auth-form">
            {!emailSent ? (
              <>
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

                <button 
                  className="auth-btn primary" 
                  onClick={handleSubmit} 
                  disabled={loading}
                >
                  {loading ? (
                    <div className="spinner"></div>
                  ) : (
                    <>
                      <span>Enviar Enlace</span>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M5 12h14m-7-7 7 7-7 7" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </>
                  )}
                </button>
              </>
            ) : (
              <div style={{ textAlign: 'center', padding: '20px 0' }}>
                <div style={{ fontSize: '48px', marginBottom: '20px' }}>📧</div>
                <p style={{ marginBottom: '10px', color: '#64748b' }}>
                  Hemos enviado un enlace de recuperación a:
                </p>
                <p style={{ fontWeight: 600, color: '#1e293b', marginBottom: '20px' }}>
                  {email}
                </p>
                <p style={{ fontSize: '14px', color: '#94a3b8' }}>
                  El enlace expirará en 1 hora. Si no ves el correo, revisa tu carpeta de spam.
                </p>
              </div>
            )}

            {message && (
              <div className={`message ${message.success ? 'success' : 'error'}`}>
                {message.message}
              </div>
            )}
          </div>

          <div className="auth-footer">
            <p>¿Recordaste tu contraseña?</p>
            <button 
              className="link-btn" 
              onClick={() => navigate('/')}
            >
              Volver al inicio de sesión
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}