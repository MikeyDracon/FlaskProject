import secrets
from datetime import datetime, timedelta


class RegistrationManager:
    def __init__(self):
        self.registration_codes = {}  # En producción, usar base de datos

    def generate_registration_code(self, expires_hours=24):
        """Generar código de registro único"""
        code = secrets.token_hex(8).upper()  # Código de 16 caracteres
        expires_at = datetime.now() + timedelta(hours=expires_hours)

        self.registration_codes[code] = {
            'expires_at': expires_at,
            'used': False,
            'max_uses': 1  # Por defecto, un solo uso
        }

        return code

    def validate_registration_code(self, code):
        """Validar código de registro"""
        if code not in self.registration_codes:
            return False, 'Código de registro inválido'

        code_data = self.registration_codes[code]

        if code_data['used']:
            return False, 'Este código ya ha sido utilizado'

        if datetime.now() > code_data['expires_at']:
            return False, 'Este código ha expirado'

        return True, 'Código válido'

    def mark_code_used(self, code):
        """Marcar código como utilizado"""
        if code in self.registration_codes:
            self.registration_codes[code]['used'] = True

    def get_active_codes(self):
        """Obtener códigos activos"""
        active_codes = {}
        for code, data in self.registration_codes.items():
            if not data['used'] and datetime.now() <= data['expires_at']:
                active_codes[code] = data
        return active_codes