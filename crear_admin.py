import os
import sys

# Agregar el directorio actual al path para que Python encuentre los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from registro.models.database import db, init_db
from registro.models.administrador import Administrador
from Config.config import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

# Inicializar la base de datos
init_db(app)


def crear_primer_administrador():
    with app.app_context():
        # Verificar si ya existe algún administrador
        if Administrador.query.first():
            print("⚠️  Ya existen administradores en la base de datos")
            return

        # Crear el primer administrador
        admin = Administrador(
            username="admin",
            email="admin@sistema.com",
            nombre_completo="Administrador Principal",
            rol="admin"  # rol con máximos privilegios
        )

        # Establecer contraseña (mínimo 6 caracteres)
        try:
            admin.set_password("admin123")  # Cambia esta contraseña
        except ValueError as e:
            print(f"❌ Error: {e}")
            return

        # Guardar en la base de datos
        db.session.add(admin)
        db.session.commit()

        print("✅ Primer administrador creado exitosamente!")
        print(f"👤 Usuario: admin")
        print(f"📧 Email: admin@sistema.com")
        print(f"🔑 Contraseña: admin123")  # Recuerda cambiar esta contraseña
        print("⚠️  IMPORTANTE: Cambia la contraseña después del primer acceso")


if __name__ == "__main__":
    crear_primer_administrador()