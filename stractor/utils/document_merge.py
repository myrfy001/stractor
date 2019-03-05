# coding:utf-8

from typing import Dict, List, Union
from collections.abc import Mapping, Sequence

DocumentTyoe = Union[Dict, List]


class ConflictAction:
    RECURSIVE = 1
    REPLACE = 2
    SKIP = 3
    NEW_LIST = 4


conflict_enum_map = {
    'recursive': ConflictAction.RECURSIVE,
    'replace': ConflictAction.REPLACE,
    'skip': ConflictAction.SKIP,
    'new_list': ConflictAction.NEW_LIST
}


def merge_doc(doc1: DocumentTyoe,
              doc2: DocumentTyoe,
              conflict: ConflictAction = ConflictAction.RECURSIVE):
    if isinstance(doc1, dict) and isinstance(doc2, dict):
        for income_key, income_doc in doc2.items():
            if income_key not in doc1:
                doc1[income_key] = income_doc
                continue

            if conflict == ConflictAction.RECURSIVE:
                doc1[income_key] = merge_doc(
                    doc1[income_key], income_doc, conflict)
            elif conflict == ConflictAction.REPLACE:
                doc1[income_key] = income_doc
            elif conflict == ConflictAction.SKIP:
                continue
            elif conflict == ConflictAction.NEW_LIST:
                doc1[income_key] = [doc1[income_key], doc2[income_key]]
    elif isinstance(doc1, list) and isinstance(doc2, list):
        for idx, income_doc in enumerate(doc1):
            doc1[idx] = merge_doc(doc1[idx], doc2[idx])
    else:
        # We assume that this is because doc1 reached the most internal level
        # if we are in a recursive context, we should return
        if conflict == ConflictAction.RECURSIVE:
            return [doc1, doc2]
        elif conflict == ConflictAction.REPLACE:
            return doc2
        elif conflict == ConflictAction.SKIP:
            return doc1
        elif conflict == ConflictAction.NEW_LIST:
            return [doc1, doc2]

    return doc1
