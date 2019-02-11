# coding:utf-8
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lxml.etree import _Element  # noqa: F401

basestring = (str, bytes)


def drop_tree(node: '_Element'):
    """
    Removes this element from the tree, including its children and
    text.  The tail text is joined to the previous element or
    parent.
    """
    parent = node.getparent()
    assert parent is not None
    if node.tail:
        previous = node.getprevious()
        if previous is None:
            parent.text = (parent.text or '') + node.tail
        else:
            previous.tail = (previous.tail or '') + node.tail
    parent.remove(node)


def drop_tag(node: '_Element'):
    """
    Remove the tag, but not its children or text.  The children and text
    are merged into the parent.
    Example::
        >>> from lxml.html import fragment_fromstring, tostring
        >>> h = fragment_fromstring('<div>Hello <b>World!</b></div>')
        >>> h.find('.//b').drop_tag()
        >>> print(tostring(h, encoding='unicode'))
        <div>Hello World!</div>
    """
    parent = node.getparent()
    assert parent is not None
    previous = node.getprevious()
    if node.text and isinstance(node.tag, basestring):
        # not a Comment, etc.
        if previous is None:
            parent.text = (parent.text or '') + node.text
        else:
            previous.tail = (previous.tail or '') + node.text
    if node.tail:
        if len(node):
            last = node[-1]
            last.tail = (last.tail or '') + node.tail
        elif previous is None:
            parent.text = (parent.text or '') + node.tail
        else:
            previous.tail = (previous.tail or '') + node.tail
    index = parent.index(node)
    parent[index:index + 1] = node[:]


def add_id_to_all_node(dom: '_Element',
                       attribute_name: str = '__stractor_dom_id'):
    for i, node in enumerate(dom.iter()):
        try:
            node.set(attribute_name, str(i))
        except Exception:
            pass
