from flaskext.mysql import MySQL

mysql = MySQL()

def init_mysql_app(app):
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = '117520123'
    app.config['MYSQL_DATABASE_DB'] = 'blogPlatformDB'
    mysql.init_app(app)
