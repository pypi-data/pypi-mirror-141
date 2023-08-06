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

#Possible workaround for multilingual sites
#from plone.app.multilingual.browser.interfaces import make_relation_root_path



class ICollectionMoveMarker(Interface):
    pass

@provider(IFormFieldProvider)
class ICollectionMove(model.Schema):
    """
    """

    linked_folder =  RelationChoice(
         title=_(u'Linked Move to Folder'),
         description=_(u'Folder to move items to'),
         required=False,
         vocabulary='plone.app.vocabularies.Catalog',
    )

    # PATTERN options might be a workaround multilingual sites
    directives.widget(
          'linked_folder',
          RelatedItemsFieldWidget,
          pattern_options={
              'selectableTypes': ['Folder'],
              #pattern_options=make_relation_root_path,
          },
     )



@implementer(ICollectionMove)
@adapter(ICollectionMoveMarker)
class CollectionMove(object):
    def __init__(self, context):
        self.context = context


    @property
    def linked_folder(self):
        if hasattr(self.context, 'linked_folder'):
            return self.context.linked_folder
        return None

    @linked_folder.setter
    def linked_folder(self, value):
            self.context.linked_folder = value
