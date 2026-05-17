import os
from flask import Flask, render_template, redirect, url_for, abort
from translations import translations
from flask import make_response 
from datetime import datetime  

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'default-key-for-dev'
)

# Поддерживаемые языки
LANGUAGES = ['pt', 'en', 'ru', 'uk']

# Основной язык сайта
DEFAULT_LANGUAGE = 'pt'


# HELPER
def get_translation(lang):

    if lang not in LANGUAGES:
        abort(404)

    return translations.get(lang, translations[DEFAULT_LANGUAGE])


def render_page(template, lang, title, description=""):

    t = get_translation(lang)

    return render_template(
        template,
        lang=lang,
        t=t,
        title=title,
        description=description
    )


# REDIRECT
@app.route('/')
def home():
    return redirect(url_for('index', lang=DEFAULT_LANGUAGE))


# INDEX
@app.route('/<lang>/')
def index(lang):

    return render_page(
        'index.html',
        lang,
        title='Oleksii Brik | Civil Engineer in Portugal',
        description='Professional Civil Engineer in Portugal. Fiscalização, construction management and licensing support.'
    )


# SERVICES
@app.route('/<lang>/services')
def services(lang):

    return render_page(
        'services.html',
        lang,
        title='Construction Services | Oleksii Brik',
        description='Fiscalização de Obra, Diretor de Obra, licensing and technical consulting in Portugal.'
    )


# PROJECTS
@app.route('/<lang>/projects')
def projects(lang):

    return render_page(
        'projects.html',
        lang,
        title='Projects and Experience | Oleksii Brik',
        description='25+ years of construction engineering experience in Portugal and international projects.'
    )


# CONTACTS
@app.route('/<lang>/contacts')
def contacts(lang):

    return render_page(
        'contacts.html',
        lang,
        title='Contact Oleksii Brik',
        description='Contact professional Civil Engineer in Lisbon, Portugal.'
    )


# ERROR 404
@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        '404.html'
    ), 404

@app.route('/robots.txt')
def robots_txt():
    content = """User-agent: *
Allow: /
Allow: /static/

Sitemap: https://oleksi-website.onrender.com/sitemap.xml
"""
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/sitemap.xml', strict_slashes=False)
def sitemap():
    base_url = "https://oleksi-website.onrender.com"
    langs = ['pt', 'en', 'ru', 'uk']
    pages_list = ['', 'services', 'projects', 'contacts'] # Добавили пустую строку для главных страниц
    
    pages = []
    today = datetime.now().strftime('%Y-%m-%d')

    for p in pages_list:
        path = f"{p}" if p else ""
        for lang in langs:
            loc = f"{base_url}/{lang}/{path}"
            
            alternates = []
            for l in langs:
                alternates.append({
                    'lang': l,
                    'href': f"{base_url}/{l}/{path}"
                })
            
            alternates.append({
                'lang': 'x-default',
                'href': f"{base_url}/pt/{path}"
            })
            
            pages.append({
                'loc': loc,
                'lastmod': today,
                'priority': '1.0' if not p else '0.8',
                'alternates': alternates
            })

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

# START
if __name__ == "__main__":
    app.run(debug=True)