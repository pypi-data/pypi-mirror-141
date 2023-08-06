class PortDescriptor:
    def __init__(self, name, default=7777):
        self.name = f'_{name}'
        self.default = default

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        value = int(value)
        if not (1024 <= value <= 65535):
            raise ValueError("Port must be from 1024 to 65535")
        setattr(instance, self.name, value)