import hashlib
import getpass
import re
import time



try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("Модуль bcrypt не установлен. Хэширование bcrypt будет недоступно.")
    print("Установите: pip install bcrypt\n")

def print_banner():
    print("=" * 70)
    print("ИНСТРУМЕНТ АНАЛИЗА ПАРОЛЕЙ И ХЭШЕЙ (EDUCATIONAL DEMO)")
    print("Этот скрипт предназначен ТОЛЬКО для обучения и тестирования своих паролей!")
    print("НЕ ИСПОЛЬЗУЙТЕ для взлома чужих аккаунтов — это незаконно.")
    print("=" * 70)
    print()

def evaluate_password_strength(password):
    score = 0
    length = len(password)

    if length >= 12:
        score += 3
    elif length >= 8:
        score += 2
    elif length >= 6:
        score += 1

    if re.search(r'[a-z]', password): score += 1
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'[0-9]', password): score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 2

    weak_patterns = ['password', 'qwerty', '123456', 'admin', 'letmein', 'welcome']
    if any(pat in password.lower() for pat in weak_patterns):
        score -= 3

    score = max(0, min(10, score))
    if score >= 8:
        return score, "Сильный пароль"
    elif score >= 5:
        return score, "Средний пароль"
    else:
        return score, "Слабый пароль — смените как можно скорее!"

def generate_hash(password, algo):
    if algo == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif algo == "sha512":
        return hashlib.sha512(password.encode()).hexdigest()
    elif algo == "bcrypt" and BCRYPT_AVAILABLE:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode('utf-8')
    else:
        return "Алгоритм не поддерживается или bcrypt не установлен"

def simple_dictionary_attack(password, dictionary):
    print("Запуск dictionary attack (демо-режим)...")
    for word in dictionary:
        if word.strip() == password:
            return True, word
        time.sleep(0.01)  
    return False, None

def main():
    print_banner()

    while True:
        print("\nМеню:")
        print("1. Проверить силу пароля")
        print("2. Сгенерировать хэши пароля")
        print("3. Демо dictionary attack (введите слабый пароль для теста)")
        print("0. Выход")
        choice = input("Выберите действие (0-3): ").strip()

        if choice == "0":
            print("До свидания! Помните: используйте сильные уникальные пароли и 2FA.")
            break

        elif choice == "1":
            password = getpass.getpass("Введите пароль для проверки: ")
            score, verdict = evaluate_password_strength(password)
            print(f"\nОценка: {score}/10 → {verdict}")
            if score < 5:
                print("Рекомендации: добавьте больше длины, заглавные буквы, цифры и символы.")

        elif choice == "2":
            password = getpass.getpass("Введите пароль для хэширования: ")
            print("\nХэши:")
            print(f"MD5:     {generate_hash(password, 'md5')}")
            print(f"SHA-256: {generate_hash(password, 'sha256')}")
            print(f"SHA-512: {generate_hash(password, 'sha512')}")
            if BCRYPT_AVAILABLE:
                print(f"bcrypt:  {generate_hash(password, 'bcrypt')}")
            print("\nMD5 и SHA устарели для хранения паролей — используйте bcrypt/Argon2!")

        elif choice == "3":
            password = getpass.getpass("Введите пароль для теста (попробуйте 'password' или '123456'): ")
            # Очень маленький словарь для демо (в реальности — rockyou.txt, но не здесь!)
            demo_dict = ["123456", "password", "qwerty", "admin", "letmein", "welcome", "abc123", "password1"]
            found, cracked = simple_dictionary_attack(password, demo_dict)
            if found:
                print(f"Пароль взломан! Это был: {cracked}")
            else:
                print("Пароль не найден в маленьком демо-словаре (это хорошо!)")
            print("В реальности атакуют миллионами слов → используйте сильные пароли!")

        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана.")
