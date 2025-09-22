from models import db, Usuario
from repositories.usuario_repo import UsuarioRepository

class UsuarioService:
    @staticmethod
    def listar_usuarios():
        usuarios = Usuario.query.all()
        return [{'id': u.id, 'email': u.email, 'nombre_completo': u.nombre_completo, 'rol_id': u.rol_id} for u in usuarios]

    @staticmethod
    def obtener_usuario(usuario_id):
        u = Usuario.query.get(usuario_id)
        if not u:
            return None
        return {'id': u.id, 'email': u.email, 'nombre_completo': u.nombre_completo, 'rol_id': u.rol_id}

    @staticmethod
    def actualizar_usuario(usuario_id, nombre=None, email=None, rol_nombre=None):
        try:
            with db.session.begin():
                u = Usuario.query.get(usuario_id)
                if not u:
                    return {'success': False, 'message': 'Usuario no encontrado'}

                if nombre:
                    u.nombre_completo = nombre
                if email:
                    u.email = email
                if rol_nombre:
                    rol = UsuarioRepository.get_rol_by_name(rol_nombre)
                    u.rol_id = rol.id
            return {'success': True, 'message': 'Usuario actualizado'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def eliminar_usuario(usuario_id):
        try:
            with db.session.begin():
                u = Usuario.query.get(usuario_id)
                if not u:
                    return {'success': False, 'message': 'Usuario no encontrado'}
                db.session.delete(u)
            return {'success': True, 'message': 'Usuario eliminado'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    @staticmethod
    def register(email, nombre, password, rol_nombre='admin'):
        try:
            with db.session.begin():  # Transacción ACID
                if UsuarioRepository.get_by_email(email):
                    return {'success': False, 'message': 'El correo ya existe'}

                rol = UsuarioRepository.get_rol_by_name(rol_nombre)
                usuario = Usuario(email=email, nombre_completo=nombre, rol_id=rol.id)
                usuario.set_password(password)
                UsuarioRepository.create(usuario)
            return {'success': True, 'message': f'Usuario {nombre} registrado como {rol_nombre}'}
        except Exception as e:
            UsuarioRepository.rollback()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def login(email, password):
        usuario = UsuarioRepository.get_by_email(email)
        if not usuario or not usuario.check_password(password):
            return {'success': False, 'message': 'Credenciales inválidas'}
        return {'success': True, 'message': f'Autenticado como {usuario.email}', 'rol': usuario.rol_id}
