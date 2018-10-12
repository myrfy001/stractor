# coding:utf-8


class DefaultTransformer:
    @classmethod
    def transform(cls, rule, doc, **kwargs):
        result = {}
        cls._build_result(result, doc, '')
        return result

    @staticmethod
    def _build_result(result: dict, doc: dict, path: str):
        path = path + '.' if path else ''
        path = path + doc['name']
        doc_value = doc['value']
        if doc_value:
            result[path] = doc_value

        for child in doc['children']:
            DefaultTransformer._build_result(result, child, path)
