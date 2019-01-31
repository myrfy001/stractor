# coding:utf-8


class ResultMeta:

    __slots__ = ('_data',)

    def __init__(self):
        self._data = {}

    @property
    def fields_group_name(self):
        return self._data.get('fields_group_name')

    @fields_group_name.setter
    def fields_group_name(self, v):
        self._data['fields_group_name'] = v

    # ========================================================================
    # 'group_to_parent_group_name_map' property is a map because children from
    # different node may have different group names and each group name may be
    # corresponding to a different parent group name

    @property
    def group_to_parent_group_name_map(self):
        return self._data.get('group_to_parent_group_name_map', {})

    @group_to_parent_group_name_map.setter
    def group_to_parent_group_name_map(self, v):
        self._data['group_to_parent_group_name_map'] = v

    @property
    def force_list(self):
        return self._data.get('force_list')

    @force_list.setter
    def force_list(self, v):
        self._data['force_list'] = v
