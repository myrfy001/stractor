# coding:utf-8


class DefaultTransformer:
    @classmethod
    def transform(cls, rule, doc, **kwargs):
        result = []
        cls._build_result(result, doc, '')
        return result

    @staticmethod
    def _build_result(result: list, doc: dict, path: str):
        values = [x for x in doc['value'] if isinstance(x, str)]
        path = path + '.' if path else ''
        path = path + doc['name']
        for value in values:
            result.append((value, path))

        for child in doc['children']:
            DefaultTransformer._build_result(result, child, path)
