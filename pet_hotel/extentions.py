from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app_mysql = MySQL(cursorclass=DictCursor)