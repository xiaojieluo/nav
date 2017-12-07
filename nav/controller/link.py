from nav import app, debug, info
from flask import render_template, url_for, session, request, flash, redirect, abort
from nav.utils import authenticated, user_themeselves
from nav.model import Link, User

@app.route('/link/<lid>')
def link(lid):
    return lid

@app.route('/link/<lid>/edit', methods = ['GET', 'POST'])
@authenticated
def link_edit(lid):
    '''编辑'''
    link = Link.find(id = lid)
    user_themeselves(link.uid)

    if request.method == 'POST':
        data = request.form.to_dict()
        debug(data)
        try:
            link.update(**data)
        except Exception as e:
            debug(e)
        flash('update successful!')
        return redirect(url_for('link_edit', lid=link.id))
    else:
        return render_template('link/edit.html', link = link)

@app.route('/link/<lid>/delete', methods = ['GET'])
@authenticated
def link_delete(lid):
    link = Link.find(id = lid)
    if link is None:
        abort(404)

    user_themeselves(link.uid)
    result = link.delete()
    if result:
        flash('删除成功')
    else:
        flash("删除失败。")
    return redirect(url_for(request.args['previous']))

@app.route('/add', methods=['GET', 'POST'])
@authenticated
def add():
    if request.method == 'POST':
        uid = session.get('uid')
        data = {
            'uid': uid,
            'username': User.find(id=uid).username
        }
        data.update(request.form.to_dict())
        debug(data)

        try:
            Link.add(**data)
        except Exception as e:
            info('添加失败:{}'.format(e))
            flash(e.args)
            return redirect(url_for('add'))
        flash('添加成功！')
        return redirect(url_for('index'))
    else:
        return render_template('link/add.html')
