from flask.ext.script import Command, Shell

#from manage import app

'''
def make_shell_context():
    bases = {m: getattr(models, m) for m in dir(models) if m[0].isupper()}
    return dict(app=app, db=db, models=models, **bases)
'''

class Hello(Command):
    "prints hello world"

    def run(self):
        print "hello world"


COMMANDS = {
    #'shell': Shell(make_context=make_shell_context),
    #'db': MigrateCommand,
    'hello': Hello(),
}
