from .config import entity_map


class TakeString:
    """
    Make clean string from dirty.
    Receive string with special chars, replace this chars by html-entity and return it.
    """
    __entity_map: dict = dict()
    __clean_string: str = str()

    def __init__(self, string: str, rule: str = 's'):
        """
        Receive dirty string and call clea n method for clean it.
        :param rule: can have value:
        - MVP: 's': string:type. It'll change all special chars by html-entity in string.
        - TO DO: EXAMPLE: ['-', ''', '"']: list:type. It'll change only specified chars in list by html-entity.
        - TO DO: EXAMPLE: [('a', 'a1'), ('b', 'b1'), ('c', 'c1')]: list:type.
        It'll change specified chars by specified rules.
        Where in every nested list specified rule to replace first char by second char from this list.
        :type rule: str:param or list:param
        """
        self.__string: str = string
        self.__rule: str = rule
        self.__entity_map = entity_map()

    def __enter__(self):
        """Provide work with context manager. Return clean string"""
        return self.make_clean_string()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Remove all created data from memory after work module"""
        if self.__entity_map:
            del self.__entity_map
        if self.__clean_string:
            del self.__clean_string
        if self.__string:
            del self.__string
        if self.__rule:
            del self.__rule
        if self.__clean_string:
            del self.__clean_string

    def make_clean_string(self) -> str:
        """Replace special charts by html-entity and return clean string."""
        if self.__rule == 's':
            for symbol in self.__string:
                if symbol in self.__entity_map:
                    self.__clean_string += self.__entity_map[symbol]
                else:
                    self.__clean_string += symbol
            return self.__clean_string
        elif type(self.__rule) is not str:
            raise TypeError(f'Rule \'{self.__rule}\' have wrong ({type(self.__rule)}) type, when need str')
        else:
            raise ValueError(f'Rule: \'{self.__rule}\' is incorrect')
