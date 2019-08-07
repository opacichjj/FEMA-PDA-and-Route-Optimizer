## these are the two app entities of our package
## the app variable 'import app' is an instance of the Flask class and thus a member of the 'app' package
from app import app, db
from app.models import User, Assessment

## decorator used to register the above imports in our shell shell_context_processor
## the shell processor is used to run code without needing imports
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Assessment': Assessment}
