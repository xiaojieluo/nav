from nav import app, debug
from nav.model import Link
from flask import render_template

@app.route('/tag/<name>')
def tag(name):
    links = Link.find_all(tags__in=[name.strip()])
    return render_template('tag/links.html', tagname = name, links = links)
    return name
