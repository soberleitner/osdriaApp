from PySide2.QtCore import *


class List(QObject):
    """representation of lists
    @param: list(Array)
    @function: add(QObject)
    @function: remove(Int)
    @signal: list_extended(QObject)
    @signal: list_reduced(Int)
    """
    list_extended = Signal()
    list_reduced = Signal(int)

    def __init__(self, list_input=[]):
        super(List, self).__init__()
        self._list = list_input

    def write(self, output):
        """write list data to output stream"""
        output.writeUInt32(len(self._list))
        for list_element in self._list:
            element_type = type(list_element)
            output.writeString(list_element.__class__.__module__)
            output.writeString(list_element.__class__.__name__)
            if element_type is str:
                output.writeString(list_element)
            elif element_type is int:
                output.writeUInt32(list_element)
            elif element_type is float:
                output.writeFloat(list_element)
            else:
                list_element.write(output)

    def read(self, input_, connection_data=None):
        """read list data from input stream"""
        list_lengths = input_.readUInt32()
        self._list = []
        for index in range(list_lengths):
            # identify class of list element
            module_name = input_.readString()
            class_name = input_.readString()
            submodules = module_name.split(".")
            if len(submodules) >= 2:
                module = __import__(module_name, fromlist=[submodules[1]])
            else:
                module = __import__(module_name)
            element_class = getattr(module, class_name)

            # distinguish between class type of list element
            if element_class == str:
                element = input_.readString()
            elif element_class == int:
                element = input_.readUInt32()
            elif element_class == float:
                element = input_.readFloat()
            else:
                element = element_class()
                element.read(input_)

            # append element to list
            self._list.append(element)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, key, value):
        self._list[key] = value

    def insert(self, index, object_):
        self._list.insert(index, object_)

    def pop(self, index):
        return self._list.pop(index)

    def __len__(self):
        return len(self._list)

    def copy(self):
        return self._list.copy()

    def add(self, value):
        self._list.append(value)
        self.list_extended.emit()

    def remove(self, item):
        self._list.remove(item)
        self.list_reduced.emit(item)

    @property
    def list(self):
        return self._list


class Dict(QObject):
    """representation of dictionary
    @param: dict(Dict)
    @function: add(QObject)
    @function: remove(str)
    @signal: dict_extended(QObject)
    @signal: dict_reduced(str)
    """
    dict_extended = Signal(QObject)
    dict_reduced = Signal(str)

    def __init__(self, dict_input={}):
        super(Dict, self).__init__()
        self._dict = dict_input

    def write(self, output):
        """write list data to output stream"""
        output.writeUInt32(len(self._dict))
        for name, list_element in self._dict.items():
            element_type = type(list_element)
            output.writeString(name)
            output.writeString(list_element.__class__.__module__)
            output.writeString(list_element.__class__.__name__)
            if element_type is str:
                output.writeString(list_element)
            elif element_type is int:
                output.writeUInt32(list_element)
            elif element_type is float:
                output.writeFloat(list_element)
            else:
                list_element.write(output)

    def read(self, input_):
        """read list data from input stream"""
        dict_lengths = input_.readUInt32()
        self._dict = {}
        for index in range(dict_lengths):
            # identify class of list element
            name = input_.readString()
            module_name = input_.readString()
            class_name = input_.readString()
            submodules = module_name.split(".")
            if len(submodules) >= 2:
                module = __import__(module_name, fromlist=[submodules[1]])
            else:
                module = __import__(module_name)
            element_class = getattr(module, class_name)

            # distinguish between class type of list element
            if element_class == str:
                element = input_.readString()
            elif element_class == int:
                element = input_.readUInt32()
            elif element_class == float:
                element = input_.readFloat()
            else:
                element = element_class()
                element.read(input_)

            # append element to list
            self._dict[name] = element

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def __len__(self):
        return len(self._dict)

    def add(self, name, value):
        self._dict[name] = value
        self.dict_extended.emit(name)

    def remove(self, name):
        del self._dict[name]
        self.dict_reduced.emit(name)

    @property
    def dict(self):
        return self._dict
