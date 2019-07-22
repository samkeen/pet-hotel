from werkzeug.exceptions import abort

from pet_hotel.db import get_db, build_insert, get_uuid, build_update, build_delete


def get_all(model_name):
    """
    simple get all models in db
    :param model_name: name of the model
    :type model_name: str
    :return:
    :rtype: list[dict]
    """
    cur = get_db().cursor()
    cur.execute(f'SELECT * FROM `{model_name}`')
    return cur.fetchall()


def insert_model(model_name, attributes):
    """
    Simple INSERT of new model to db
    :param model_name:
    :type model_name: str
    :param attributes:
    :type attributes: dict
    :return:
    :rtype: None
    """
    attributes.pop('csrf_token', None)
    cur = get_db().cursor()
    insert_query = build_insert(model_name, attributes)
    values = tuple(n for n in [get_uuid()] + list(attributes.values()))
    cur.execute(insert_query, values)
    get_db().commit()


def get_model_by_id(model_name, model_id):
    """

    :param model_name:
    :type model_name: str
    :param model_id:
    :type model_id: str
    :return:
    :rtype: dict
    """
    cur = get_db().cursor()
    cur.execute(f'SELECT * FROM `{model_name}` WHERE `id` = %s', (model_id,))
    model = cur.fetchone()
    if model is None:
        abort(404, f"{model_name} id {0} doesn't exist.".format(model_id))
    return model


def update_model(model_name, model_id, attributes):
    """

    :param model_name:
    :type model_name: str
    :param model_id:
    :type model_id: str
    :param attributes:
    :type attributes: dict
    :return:
    :rtype:
    """
    attributes.pop('csrf_token', None)
    attributes.pop('id', None)
    cur = get_db().cursor()
    update_query = build_update(model_name, attributes)
    values = tuple(n for n in list(attributes.values()) + [model_id])
    cur.execute(update_query, values)
    get_db().commit()


def delete_model(model_name, model_id):
    """

    :param model_name:
    :type model_name: str
    :param model_id:
    :type model_id: str
    :return:
    :rtype: None
    """
    cur = get_db().cursor()
    cur.execute(build_delete(model_name), (model_id,))
    get_db().commit()


class ObjectView(object):
    """
    Give a dict attribute accessors
    Needed for WTForms
    """

    def __init__(self, d):
        self.__dict__ = d
