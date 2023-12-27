class BaseLM(object):

    def __init__(self, name):
        self.__name = name

    def ask(self, prompt):
        raise NotImplemented()
