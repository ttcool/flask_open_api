# coding:utf-8

from flask_script import Manager,Server
from main import app,db,Article

manger=Manager(app)
manger.add_command("server",Server)
@manger.shell
def make_shell_context():
    return dict(app=app,db=db,Article=Article)

if __name__=="__main__":
    manger.run()