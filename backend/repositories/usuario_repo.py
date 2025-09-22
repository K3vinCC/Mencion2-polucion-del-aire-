from models import db, Usuario, Rol

class UsuarioRepository:
    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def create(usuario: Usuario):
        db.session.add(usuario)
        db.session.flush()  # genera ID antes del commit
        return usuario

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()

    @staticmethod
    def get_rol_by_name(nombre):
        rol = Rol.query.filter_by(nombre=nombre).first()
        if not rol:
            rol = Rol(nombre=nombre)
            db.session.add(rol)
            db.session.flush()
        return rol
