# coding:utf-8

from .exceptions import QuerierNotSupported


class Transformer:

    REGISTERED_TRANSFORMER_CLASSES = {}

    @classmethod
    def register_transformer(cls, name, clazz):
        cls.REGISTERED_TRANSFORMER_CLASSES[name] = clazz

    def __init__(self, transformer_item):
        self.type = transformer_item.get('type', 'default')

        self.rule = transformer_item.get('rule', '')

        self.transformer_class = self.REGISTERED_TRANSFORMER_CLASSES.get(
            self.type)
        if self.transformer_class is None:
            raise QuerierNotSupported(self.type)

    def transform(self, doc, **kwargs):
        return self.transformer_class.transform(self.rule, doc, **kwargs)
