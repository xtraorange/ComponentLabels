from Logger import Logger

class TypedAttributes:
    _attributes = {}

    @classmethod
    def get_all_attributes(cls):
        """ Recursively get _attributes from current and parent classes """
        attributes = {}
        for base in reversed(cls.__mro__):
            if issubclass(base, TypedAttributes) and hasattr(base, '_attributes'):
                attributes.update(base._attributes)
        return attributes

    def __init__(self):
        self.__dict__['_attributes'] = self.get_all_attributes()

    def __setattr__(self, name, value):
        if self._is_property(name):
            # Use the property setter
            property_obj = type(self).__dict__[name]
            if property_obj.fset is None:
                raise AttributeError(f"Can't set attribute '{name}'")
            property_obj.fset(self, value)
        else:
            self._set_regular_attribute(name, value)

    def _set_regular_attribute(self, name, value):
        attributes = getattr(self, '_attributes', {})
        if name in attributes:
            attribute_type, default_value = attributes[name]
            Logger.debug(f"Setting property: {name} of type: {attribute_type.__name__} with value: {value}")
            if not isinstance(value, attribute_type) and value is not None:
                try:
                    value = attribute_type(value)
                except (ValueError, TypeError):
                    raise TypeError(f"'{name}' must be of type {attribute_type.__name__}")
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        if self._is_property(name):
            # Use the property getter
            return object.__getattribute__(self, name).fget(self)
        else:
            return self._get_regular_attribute(name)

    def _get_regular_attribute(self, name):
        attributes = getattr(self, '_attributes', {})
        if name in attributes:
            return attributes[name][1]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def _is_property(self, name):
        """ Check if an attribute name is a property """
        return isinstance(getattr(type(self), name, None), property)

    def set_attribute(self, **kwargs):
        for name, value in kwargs.items():
            if hasattr(self, name) or self._is_property(name):
                setattr(self, name, value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return self