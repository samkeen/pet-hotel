import uuid

from flask import current_app, g

from pet_hotel.extentions import app_mysql


def get_db():
    if 'db' not in g:
        g.db = app_mysql.connect()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_uuid():
    return str(uuid.uuid1())


def build_insert(table_name, attributes):
    attributes.pop('id', None)  # don't allow id to be set
    field_names = attributes.keys()
    field_values = attributes.values()
    fields = f'INSERT INTO `{table_name}` (`id`, `{"`, `".join(field_names)}`)'
    values = f'VALUES ( %s, {", ".join(["%s"] * len(field_values))})'
    return f'{fields} {values}'


def build_update(table_name, attributes):
    attributes.pop('id', None)  # don't allow id in attributes
    set_statements = [f'`{k}`= %s' for k in attributes.keys()]
    return f'UPDATE `{table_name}` SET {", ".join(set_statements)} WHERE id = %s'


def build_delete(table_name):
    return f'DELETE FROM `{table_name}` WHERE id = %s'
