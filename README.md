🚀 Встановлення

git clone https://github.com/WindStorm24/LinkedIn_Parser.git
cd linkedin-scraper

Створити віртуальне середовище (рекомендується)

python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows

Встановити залежності

pip install -r requirements.txt

⚙️ Налаштування

    Додати проксі у proxies.txt (по одному на рядок у форматі ip:port або user:pass@ip:port для SOCKS5).
    Запустити скрипт

python main.py

🛠 Функціонал

✅ Авторизація в LinkedIn за логіном і паролем.
✅ Парсинг фото профілю користувача за його username.
✅ Автоматична обробка капчі шляхом зміни IP (проксі).
✅ Логування подій у файл out.log.
📝 Формат введення

При запуску скрипта потрібно ввести:

    Логін (email від LinkedIn)
    Пароль
    Ім'я профілю (наприклад, denis-holovkin-3a2139339)

📥 Результат

Фото профілю зберігається у файл profile_picture.jpg.
🔧 Можливі помилки

    Невірні облікові дані → Перевір логін/пароль.
    Доступ заборонений → LinkedIn може тимчасово заблокувати вхід, спробуй змінити IP через VPN або проксі.
    Помилка драйвера Chrome → Переконайся, що встановлена остання версія undetected_chromedriver.
