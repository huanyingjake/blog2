"""
这个文件，是模块的初始文件，每次载入模块时候，就会运行了。所以，当运行flask flaskr时候，就会运行这个程序
"""

import os
from flask import Flask


# 工厂函数，可以返回一个 flask的app实例
def create_app(test_config=None):
    # 新建一个Flask实例
    app = Flask(__name__, instance_relative_config=True)

    # app的参数。SECRET_KEY用于生成密码，可能是session时候加密
    # DATABASE是设置数据库的名称。os.path.join拼接 路径和文件名
    # app.instance_path，是实例文件夹，用于保存数据的。不把它当作程序的一部分。实现程序和数据的分离
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # 设置config文件，如果参数没有，就载入config.py文件，如果config.py都没有，那就什么都没有。
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)  # load the instance config,if it exists, when not testing
    else:
        # 这个用来载入测试参数
        app.config.from_mapping(test_config)  # load the test config if passed in

    # 新建实例文件夹（用于存放数据）
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 测试用的网页
    @app.route('/hello')
    def hello():
        return 'hello worldsdffs'

    # 载入初始化的程序。初始化一个数据库，并且把命令行，绑定到这个实例上
    from . import db
    db.init_app(app)

    # 把auth的蓝图，加载到主的app模块中去。
    from . import auth
    app.register_blueprint(auth.bp)

    # 把blog蓝图，放到主的app中去
    from . import blog
    app.register_blueprint(blog.bp)
    # 这个还不是很懂
    app.add_url_rule('/', endpoint='index')

    # 返回主的app实例
    return app
