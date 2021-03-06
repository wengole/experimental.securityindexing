from plone import api

from .interfaces import IShadowTreeTool


def _shadowtree_node_for_content(obj):
    portal = api.portal.get()
    site = portal.getSiteManager()
    root = site.getUtility(IShadowTreeTool).root
    return root.ensure_ancestry_to(obj)


def on_object_added(obj, event):
    """Synchronise shadowtree security info for corresponding content.

    :param obj: The content object.
    :param event: The event.
    """
    node = _shadowtree_node_for_content(obj)
    node.update_security_info(obj)
    assert node.physical_path == obj.getPhysicalPath()


def on_object_removed(obj, event):
    """Synchronise shadowtree security info for corresponding content.

    :param obj: The content object.
    :param event: The event.
    """
    node = _shadowtree_node_for_content(obj)
    parent = node.__parent__
    if parent is not None and obj.getId() in parent:
        del parent[obj.getId()]
