# coding:utf-8

from flask_script import Manager,Server
from main import app,db,Article

manager=Manager(app)
manager.add_command("server",Server)
@manager.shell
def make_shell_context():
    return dict(app=app,db=db,Article=Article)

if __name__=="__main__":
    manager.run()