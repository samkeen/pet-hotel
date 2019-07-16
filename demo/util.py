class ObjectView(object):
    """
    Give a dict attribute accessors
    """
    def __init__(self, d):
        self.__dict__ = d