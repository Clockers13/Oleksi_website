from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('contacts.html', title="Контакты")

if __name__ == "__main__":
    app.run(debug=True)
