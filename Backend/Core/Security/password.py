import string
import secrets

def generate_password(length: int) -> str:
    if length < 8:
        raise ValueError("Длина безопасного пароля должна быть не менее 8 символов.")

    letters_lowercase = string.ascii_lowercase
    letters_uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    all_characters = letters_lowercase + letters_uppercase + digits + special_chars

    password = [
        secrets.choice(letters_lowercase),
        secrets.choice(letters_uppercase),
        secrets.choice(digits),
        secrets.choice(special_chars)
    ]

    password += [secrets.choice(all_characters) for _ in range(length - 4)]

    secrets.SystemRandom().shuffle(password)
    return "".join(password)