from nav import app, debug
from flask import render_template
from nav.model import Link

@app.route('/')
@app.route('/index')
def index():
    links = Link.find_all()
    return render_template('index.html', links = links)

@app.route('/news')
def news():
    '''
    最新
    '''
    links = Link.find_all(sort='-created_at')
    return render_template('index.html', links = links)


@app.route('/hot')
def hot():
    '''
    最热
    '''
    links = Link.find_all()
    return render_template('index.html', links = links)
