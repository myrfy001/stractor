# coding:utf-8


class MetaBase:
    pass


class DomMeta(MetaBase):
    __slots__ = ()


class ResultMeta(MetaBase):

    __slots__ = ('_fields_group_name',
                 '_force_list', '_has_merged_data', '_merge_conflict')

    def __init__(self):
        self._fields_group_name = None
        self._force_list = True
        self._has_merged_data = False

        # can be 'recursive', 'replace', 'merge', 'ignore'
        self._merge_conflict = 'recursive'

    @property
    def fields_group_name(self):
        return self._fields_group_name

    @fields_group_name.setter
    def fields_group_name(self, v):
        self._fields_group_name = v

    @property
    def merge_conflict(self):
        return self._merge_conflict

    @merge_conflict.setter
    def merge_conflict(self, v):
        self._merge_conflict = v

    @property
    def force_list(self):
        return self._force_list

    @force_list.setter
    def force_list(self, v):
        self._force_list = v

    @property
    def has_merged_data(self):
        return self._has_merged_data

    @has_merged_data.setter
    def has_merged_data(self, v):
        self._has_merged_data = v
