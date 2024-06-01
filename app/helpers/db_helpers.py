from django.db import connection


def db_enable_long_query(timeout=0):
    cs = connection.cursor()
    cs.execute("set statement_timeout={};".format(timeout))
