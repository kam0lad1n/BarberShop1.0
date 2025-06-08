from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def validate(self, password, user=None):

        if len(password) < 8:
            raise ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")

        if password.isdigit():
            raise ValidationError("Parol to‘liq raqamlardan iborat bo‘lishi mumkin emas.")

        common_passwords = ['123456', 'password', 'qwerty', '111111']
        if password.lower() in common_passwords:
            raise ValidationError("Bu parol juda keng tarqalgan.")

    def get_help_text(self):
        return "Parol kuchli va noyob bo‘lishi kerak."
