import functools

# flask实例需要用到的对象
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# 密码设置
from werkzeug.security import check_password_hash, generate_password_hash

# 这个连接数据库
from flaskr.db import get_db

# 新建一个蓝图，名称是auth;文件位置是当前（__name__);路径前缀是"/auth",所有的路径，还要加上这个
bp = Blueprint('auth', __name__, url_prefix="/auth")


# 蓝图建立一个路由
@bp.route('/register', methods=('GET', 'POST'))
# 路由的方法
def register():
    # 如果是表格提交，那么注册。
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        print(db)
        error = None

        if not username:
            error = 'Username is required. '
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username,password) VALUES (?,?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                print(type(db))
            except db.IntegrityError:
                error = f"User {username} is already registered ."
            else:
                # 没有出发异常，那么就执行登录
                return redirect(url_for("auth.login"))
        # flash() 用于储存在渲染模块时可以调用的信息。
        flash(error)
    # 如果是get，那么就显示注册页面
    return render_template('auth/register.html')


# 蓝图的第二个路由
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrent password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

    return render_template('auth/login.html')


# bp蓝图的第三个路由
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    这个装饰器，看了很久才看明白。
    首先，会返回wrapped_view函数，运行这个函数。
    运行wrapped_view这个部分
            if g.user is None:
            return redirect(url_for('auth.login'))
    然后wwrapped_view函数，返回view函数。view函数是修饰器下面的函数，就是运行@login_required下面的函数。

    这里的@functools.wraps(view),会把@login_required下方的函数的__name__为本身，就是跟login_required无关的。
    案例如下

    from functools import wraps
    def wrap1(func):
        @wraps(func)	# 去掉就会返回inner
        def inner(*args):
            print(func.__name__)
            return func(*args)
        return inner

    @wrap1
    def demo():
        print('hello world')

    print(demo.__name__)
    # demo

    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
