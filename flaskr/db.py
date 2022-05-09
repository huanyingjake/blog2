import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # 这个open_resource是打开相对于flaskr包的
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# 这个可以使用 flask init-db 来执行命令行工具。装饰器把init_db_command函数给外面
@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database .')


def init_app(app):
    # 告诉flask，在返回响应后，进行清理的时候，调用这个函数
    app.teardown_appcontext(close_db)

    # 添加一个可以与flask一起工作的命令
    app.cli.add_command(init_db_command)
