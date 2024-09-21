def handle_uploaded_file(f):
    with open(f"media/photos/photos_users/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


import re

def validate_password(password):
    """
    Проверяет, соответствует ли пароль следующим требованиям:
    - Длина пароля должна быть не менее 8 символов
    - Пароль должен содержать как минимум одну цифру
    """
    
    # Проверка длины пароля
    if len(password) < 8:
        return False, "Пароль должен быть не менее 8 символов"
    
    # Проверка наличия цифры
    if not re.search(r'\d', password):
        return False, "Пароль должен содержать как минимум одну цифру"
    
    
    # Если все проверки пройдены, возвращаем True
    return True, "Пароль соответствует требованиям"