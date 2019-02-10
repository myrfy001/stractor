# coding:utf-8


class ResultMeta:

    __slots__ = ('_fields_group_name',
                 '_force_list', '_has_merged_data')

    def __init__(self):
        self._fields_group_name = {}
        self._force_list = True
        self._has_merged_data = False

    @property
    def fields_group_name(self):
        return self._fields_group_name

    @fields_group_name.setter
    def fields_group_name(self, v):
        self._fields_group_name = v

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
