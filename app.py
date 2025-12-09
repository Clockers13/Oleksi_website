import os
from flask import Flask, render_template

app = Flask(__name__)

# Секретный ключ можно оставить на всякий случай, но для Formspree он не критичен
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key-for-dev')

@app.route('/')
def index():
    return render_template('index.html', title="Главная")

@app.route('/services')
def services():
    return render_template('services.html', title="Услуги")

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Проекты")

@app.route('/contacts')
def contacts():
    # Теперь мы просто показываем страницу. 
    # Обработку формы берет на себя Formspree (через action в HTML).
    return render_template('contacts.html', title="Контакты")

if __name__ == "__main__":
    app.run(debug=True)