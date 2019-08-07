from flask import render_template  ## loading 'render_template' to send this to html pages
from app import app, db  ## loading our application and database

## creating our 404 error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

## creating our 500 error
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  ## this prevents any incorrect interference with our database by rolling back the session to a clean slate
    return render_template('500.html'), 500
