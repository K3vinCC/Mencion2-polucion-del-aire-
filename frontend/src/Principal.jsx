import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './principal.css';

function UsuarioModel({ id = null, nombre_completo = '', email = '', rol = 'admin' } = {}) {
  return { id, nombre_completo, email, rol };
}

class UsuarioAdapter {
  constructor(baseURL = 'http://localhost:5000') {
    this.baseURL = baseURL;
  }

  async listarUsuarios() {
    try {
      const res = await fetch(`${this.baseURL}/usuario/listar`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();
      
      if (data.success && data.usuarios) {
        const usuariosMapeados = data.usuarios.map(usuario => ({
          id: usuario.id,
          nombre_completo: usuario.nombre_completo,
          email: usuario.email,
          rol: usuario.rol_id === 2 ? 'admin' : 'conserje'
        }));
        return { success: true, usuarios: usuariosMapeados };
      }
      return data;
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  async crearUsuario({ nombre_completo, email, password, rol }) {
    try {
      const res = await fetch(`${this.baseURL}/usuario/crear`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          nombre_completo, 
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

  async actualizarUsuario(id, { nombre_completo, email, rol }) {
    try {
      const res = await fetch(`${this.baseURL}/usuario/${id}/actualizar`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          nombre_completo, 
          email, 
          rol 
        })
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }

  async eliminarUsuario(id) {
    try {
      const res = await fetch(`${this.baseURL}/usuario/${id}/eliminar`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: 'Error de conexión al servidor' };
    }
  }
}

class ListarUsuariosUseCase {
  constructor(usuarioAdapter) {
    this.usuarioAdapter = usuarioAdapter;
  }

  async execute() {
    return await this.usuarioAdapter.listarUsuarios();
  }
}

class CrearUsuarioUseCase {
  constructor(usuarioAdapter) {
    this.usuarioAdapter = usuarioAdapter;
  }

  async execute(usuarioData) {
    if (!usuarioData.email.includes('@')) {
      return { success: false, message: 'Email inválido' };
    }
    if (usuarioData.password.length < 6) {
      return { success: false, message: 'La contraseña debe tener al menos 6 caracteres' };
    }
    return await this.usuarioAdapter.crearUsuario(usuarioData);
  }
}

class ActualizarUsuarioUseCase {
  constructor(usuarioAdapter) {
    this.usuarioAdapter = usuarioAdapter;
  }

  async execute(id, usuarioData) {
    if (!usuarioData.email.includes('@')) {
      return { success: false, message: 'Email inválido' };
    }
    return await this.usuarioAdapter.actualizarUsuario(id, usuarioData);
  }
}

class EliminarUsuarioUseCase {
  constructor(usuarioAdapter) {
    this.usuarioAdapter = usuarioAdapter;
  }

  async execute(id) {
    return await this.usuarioAdapter.eliminarUsuario(id);
  }
}

class UsuarioController {
  constructor() {
    this.adapter = new UsuarioAdapter();
    this.listarUseCase = new ListarUsuariosUseCase(this.adapter);
    this.crearUseCase = new CrearUsuarioUseCase(this.adapter);
    this.actualizarUseCase = new ActualizarUsuarioUseCase(this.adapter);
    this.eliminarUseCase = new EliminarUsuarioUseCase(this.adapter);
  }

  async listarUsuarios() {
    return await this.listarUseCase.execute();
  }

  async crearUsuario(usuarioData) {
    return await this.crearUseCase.execute(usuarioData);
  }

  async actualizarUsuario(id, usuarioData) {
    return await this.actualizarUseCase.execute(id, usuarioData);
  }

  async eliminarUsuario(id) {
    return await this.eliminarUseCase.execute(id);
  }
}

function UsuarioModal({ isOpen, onClose, usuario, onSave, title }) {
  const [formData, setFormData] = useState(UsuarioModel());
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    if (usuario) {
      setFormData(usuario);
    } else {
      setFormData(UsuarioModel());
    }
    setMessage(null);
  }, [usuario, isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    const result = await onSave(formData);
    
    setLoading(false);
    
    if (result.success) {
      onClose();
    } else {
      setMessage(result);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>Nombre Completo</label>
            <input
              type="text"
              value={formData.nombre_completo}
              onChange={(e) => setFormData({...formData, nombre_completo: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>

          {!usuario && (
            <div className="form-group">
              <label>Contraseña</label>
              <input
                type="password"
                value={formData.password || ''}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
              />
            </div>
          )}

          <div className="form-group">
            <label>Rol</label>
            <select
              value={formData.rol}
              onChange={(e) => setFormData({...formData, rol: e.target.value})}
            >
              <option value="admin">Administrador</option>
              <option value="conserje">Conserje</option>
            </select>
          </div>

          {message && (
            <div className={`message ${message.success ? 'success' : 'error'}`}>
              {message.message}
            </div>
          )}

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancelar
            </button>
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function Principal() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingUsuario, setEditingUsuario] = useState(null);
  const [message, setMessage] = useState(null);
  const [userInfo, setUserInfo] = useState(null);

  const navigate = useNavigate();
  const controller = new UsuarioController();

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/');
      return;
    }
    
    const user = JSON.parse(userData);
    setUserInfo(user);
    
    cargarUsuarios();
  }, [navigate]);

  const cargarUsuarios = async () => {
    setLoading(true);
    const result = await controller.listarUsuarios();
    setLoading(false);

    if (result.success) {
      setUsuarios(result.usuarios);
    } else {
      setMessage({ success: false, message: result.message });
    }
  };

  const handleCrearUsuario = async (usuarioData) => {
    const result = await controller.crearUsuario(usuarioData);
    if (result.success) {
      await cargarUsuarios();
      setMessage({ success: true, message: 'Usuario creado exitosamente' });
    }
    return result;
  };

  const handleEditarUsuario = async (usuarioData) => {
    const result = await controller.actualizarUsuario(usuarioData.id, usuarioData);
    if (result.success) {
      await cargarUsuarios();
      setMessage({ success: true, message: 'Usuario actualizado exitosamente' });
    }
    return result;
  };

  const handleEliminarUsuario = async (id) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
      return;
    }

    const result = await controller.eliminarUsuario(id);
    if (result.success) {
      await cargarUsuarios();
      setMessage({ success: true, message: 'Usuario eliminado exitosamente' });
    } else {
      setMessage({ success: false, message: result.message });
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/');
  };

  const openCreateModal = () => {
    setEditingUsuario(null);
    setModalOpen(true);
  };

  const openEditModal = (usuario) => {
    setEditingUsuario(usuario);
    setModalOpen(true);
  };

  const getRoleBadgeClass = (rol) => {
    return rol === 'admin' ? 'role-badge admin' : 'role-badge conserje';
  };

  const getRoleText = (rol) => {
    return rol === 'admin' ? 'Administrador' : 'Conserje';
  };

  return (
    <div className="principal-container">
      <header className="principal-header">
        <div className="header-content">
          <h1>EcoAula UCT - Panel de Administración</h1>
          <div className="user-info">
            <span>Bienvenido, {userInfo?.email}</span>
            <span className={getRoleBadgeClass(userInfo?.rol)}>
              {getRoleText(userInfo?.rol)}
            </span>
            <button onClick={handleLogout} className="logout-btn">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      <main className="principal-content">
        <div className="content-header">
          <h2>Gestión de Usuarios</h2>
          <button onClick={openCreateModal} className="btn-primary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M12 5v14m-7-7h14" stroke="currentColor" strokeWidth="2"/>
            </svg>
            Crear Usuario
          </button>
        </div>

        {message && (
          <div className={`alert ${message.success ? 'success' : 'error'}`}>
            {message.message}
            <button onClick={() => setMessage(null)} className="close-alert">×</button>
          </div>
        )}

        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Cargando usuarios...</p>
          </div>
        ) : (
          <div className="usuarios-grid">
            {usuarios.length === 0 ? (
              <div className="empty-state">
                <p>No hay usuarios registrados</p>
                <button onClick={openCreateModal} className="btn-primary">
                  Crear primer usuario
                </button>
              </div>
            ) : (
              usuarios.map(usuario => (
                <div key={usuario.id} className="usuario-card">
                  <div className="usuario-info">
                    <div className="usuario-avatar">
                      {usuario.rol === 'admin' ? '👨‍💼' : '🔧'}
                    </div>
                    <div className="usuario-details">
                      <h3>{usuario.nombre_completo}</h3>
                      <p>{usuario.email}</p>
                      <span className={getRoleBadgeClass(usuario.rol)}>
                        {getRoleText(usuario.rol)}
                      </span>
                    </div>
                  </div>
                  <div className="usuario-actions">
                    <button 
                      onClick={() => openEditModal(usuario)}
                      className="btn-edit"
                      title="Editar usuario"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" strokeWidth="2"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </button>
                    <button 
                      onClick={() => handleEliminarUsuario(usuario.id)}
                      className="btn-delete"
                      title="Eliminar usuario"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <polyline points="3,6 5,6 21,6" stroke="currentColor" strokeWidth="2"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="currentColor" strokeWidth="2"/>
                        <line x1="10" y1="11" x2="10" y2="17" stroke="currentColor" strokeWidth="2"/>
                        <line x1="14" y1="11" x2="14" y2="17" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </main>

      <UsuarioModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        usuario={editingUsuario}
        onSave={editingUsuario ? handleEditarUsuario : handleCrearUsuario}
        title={editingUsuario ? 'Editar Usuario' : 'Crear Usuario'}
      />
    </div>
  );
}