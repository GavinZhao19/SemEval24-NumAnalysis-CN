import importlib


def auto_import(name, is_class=False):
    """ Import from the external python packages.
    """
    def __get_module(comps_list):
        return importlib.import_module(".".join(comps_list))

    components = name.split('.')
    m = getattr(__get_module(components[:-1]), components[-1])

    return m() if is_class else m


class TxtService:

    @staticmethod
    def read_lines(filepath):
        print("Opening file: {}".format(filepath))
        with open(filepath, "r") as f:
            return [line.strip() for line in f.readlines()]