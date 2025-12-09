import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

# Загружаем переменные из скрытого файла .env
load_dotenv()

app = Flask(__name__)

# --- КОНФИГУРАЦИЯ (Берется из файла .env) ---
# Secret Key нужен для работы flash-сообщений (уведомлений об успехе)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Настройки почты Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# Если вдруг email не отправляется, вывод ошибок поможет понять почему
app.config['MAIL_DEBUG'] = True 

mail = Mail(app)

# --- МАРШРУТЫ ---

@app.route('/')
def index():
    return render_template('index.html', title="Главная")

@app.route('/services')
def services():
    return render_template('services.html', title="Услуги")

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Проекты")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        # 1. Сбор данных из формы
        name = request.form.get('name')
        phone = request.form.get('phone')
        message_body = request.form.get('message')

        # 2. Создание письма
        # Письмо придет от ВАС (MAIL_USERNAME) к ВАМ ЖЕ (recipients)
        msg = Message(
            subject=f"Новая заявка: {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']] # Можно добавить сюда email менеджера через запятую
        )
        
        # Текст письма
        msg.body = f"""
        Вам поступила новая заявка с сайта.
        
        Имя клиента: {name}
        Телефон: {phone}
        
        Сообщение:
        {message_body}
        """

        # 3. Попытка отправки
        try:
            mail.send(msg)
            flash('Спасибо! Ваше сообщение отправлено. Я свяжусь с вами в ближайшее время.', 'success')
            return redirect(url_for('contacts'))
        except Exception as e:
            # Если ошибка (например, неверный пароль), покажем её на экране
            flash(f'Ошибка при отправке сообщения: {str(e)}', 'error')

    return render_template('contacts.html', title="Контакты")

if __name__ == "__main__":
    app.run(debug=True)