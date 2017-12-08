from nav import app, debug, info
from nav.model import User, Link
from flask import render_template, request, flash, redirect, url_for, session
from pymongo.errors import DuplicateKeyError
from mongoengine.errors import NotUniqueError
import json
from flask.views import MethodView
from nav.utils import authenticated, user_themeselves

@app.route('/users/<uid>', methods=['GET', 'POST'])
def user(uid):
    if request.method == 'POST':
        data = request.form.to_dict()
        if data:
            User.update(**data)
    else:
        user = User.find(id = uid)
        debug(user)
        if user is not None:
            # if user.id == session.get('uid', None):
            #     # 查看的用户主页是当前已登陆用户
            return render_template('user/index.html', user = user)
        else:
            abort(404)

@app.route('/users/<uid>/edit', methods = ['GET', 'POST'])
@authenticated
def user_edit(uid):
    '''
    编辑自己的用户详情
    '''
    user_themeselves(uid)
    if request.method == 'POST':
        data = request.form.to_dict()
        if data:
            user = User.find(id = uid)
            if user:
                user.update(**data)
                flash('更新成功。')
            else:
                flash('用户不存在')
            return redirect(url_for('user_edit', uid = user.id))
    else:
        user = User.find(id = uid)
        return render_template('user/edit.html', user = user)

@app.route('/users/<uid>/links', methods = ['GET'])
@authenticated
def user_links(uid):
    '''
    显示自己的所有链接
    '''
    links = Link.find_all(uid = session.get('uid'))
    return render_template('user/links.html', links = links)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    user login
    '''
    if request.method == 'POST':
        data = request.form.to_dict()
        user = User.login(**data)
        if user is not None:
            info("{} login successful!".format(user.username))
            session['username'] = user.username
            session['uid'] = str(user.id)
            flash('login successful')
            if 'next' in request.args:
                return redirect(request.args['next'])
            else:
                return redirect(url_for('index'))
        else:
            # info('{} login failed.'.format(data['username']))
            flash('{} login failed.'.format(data['username']))
            return render_template('user/login.html')
    else:
        return render_template('user/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    user register
    '''
    if request.method == 'POST':
        data = request.form.to_dict()
        if data:
            try:
                User.register(**data)
            except NotUniqueError as e:
                info("注册失败:{}".format(e))

                flash('register failed: {}'.format(e.args))
                return redirect(url_for('register'))

        flash("register successful.")
        info("注册成功")
        return redirect(url_for('register'))
    else:
        return render_template('user/register.html')

@app.route('/logout')
def logout():
    '''
    user logout
    '''
    session.pop('uid', None)
    session.pop('username', None)
    flash('logout successful.')
    return redirect(url_for('index'))
