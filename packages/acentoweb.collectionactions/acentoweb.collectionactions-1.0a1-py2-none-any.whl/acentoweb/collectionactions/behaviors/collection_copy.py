# -*- coding: utf-8 -*-

from acentoweb.collectionactions import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from plone.autoform import directives
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.vocabularies.catalog import CatalogSource


class ICollectionCopyMarker(Interface):
    pass

@provider(IFormFieldProvider)
class ICollectionCopy(model.Schema):
    """
    """

    linked_copy_folder =  RelationChoice(
         title=_(u'Linked Copy folder'),
         description=_(u'Folder to copy items to'),
         required=False,
         vocabulary='plone.app.vocabularies.Catalog',
    )

    directives.widget(
          'linked_copy_folder',
          RelatedItemsFieldWidget,
          pattern_options={
              'selectableTypes': ['Folder'],
              #pattern_options=make_relation_root_path,
          },
     )



@implementer(ICollectionCopy)
@adapter(ICollectionCopyMarker)
class CollectionCopy(object):
    def __init__(self, context):
        self.context = context

    @property
    def linked_copy_folder(self):
        if hasattr(self.context, 'linked_copy_folder'):
            return self.context.linked_copy_folder
        return None

    @linked_copy_folder.setter
    def linked_copy_folder(self, value):
        self.context.linked_copy_folder = value
