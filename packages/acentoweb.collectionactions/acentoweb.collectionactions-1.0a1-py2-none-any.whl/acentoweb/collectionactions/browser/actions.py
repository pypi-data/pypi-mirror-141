# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zExceptions import Unauthorized
from zope.event import notify
from zope.interface import Interface
import transaction


from plone import api

#Potential needed imports
#import six
#from OFS.CopySupport import CopyError
#from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.CMFPlone.utils import safe_unicode
#from ZODB.POSException import ConflictError
#from z3c.form import button
#from z3c.form import field
#from z3c.form import form
#from z3c.form.widget import ComputedWidgetAttribute
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.lifecycleevent import ObjectModifiedEvent
#from zope import schema
#from zope.component import getMultiAdapter
#from zope.component import queryMultiAdapter
#from zope.container.interfaces import INameChooser

class CollectionMove(BrowserView):

    def __call__(self):
        messages = IStatusMessage(self.request)
        context = self.context

        #Get folder we move the object  to
        to_folder = context.linked_folder.to_object

        ## TO DO: Check if any item is locked ??
        #plone.api.content.move(source=None, target=None, id=None, safe_id=False)[source]¶
        #Move the object to the target container.

        #Parameters
        #source (Content object) – [required] Object that we want to move.
        #target (Folderish content object) – Target container to which the source object will be moved. If no target is specified, the source object’s container will be used as a target, effectively making this operation a rename (Rename content).
        #id (string) – Pass this parameter if you want to change the id of the moved object on the target location. If the new id conflicts with another object in the target container, a suffix will be added to the moved object’s id.
        #safe_id (boolean) – When False, the given id will be enforced. If the id is conflicting with another object in the target container, raise a InvalidParameterError. When True, choose a new, non-conflicting id.

        #Returns
        #Content object that was moved to the target location

        #Raises
        #KeyError ValueError

        #portal = api.portal.get()

        #except KeyError:
        #    messages.add(u"Folder does not exist", type="warning")

        if to_folder:

            for item in  context.restrictedTraverse('@@contentlisting')():
                try:
                    api.content.move(source=item.getObject(), target=to_folder)
                    messages.add('Moved item: ' + item.id + ' to folder: ' + to_folder.Title(), type="info")
                except KeyError:
                    messages.add(u"Folder does not exist", type="warning")

        else:
            messages.add(u'Nothing to move', type="info")

        self.request.response.redirect(context.absolute_url())



class CollectionCopy(BrowserView):

    def __call__(self):
        messages = IStatusMessage(self.request)
        context = self.context

        to_folder = context.linked_folder.to_object

        if to_folder:
            for item in  context.restrictedTraverse('@@contentlisting')():
                try:
                    api.content.copy(source=item.getObject(), target=to_folder)
                    messages.add('Copied item: ' + item.id + ' to folder: ' + to_folder.Title(), type="info")
                except KeyError:
                    messages.add(u"Folder does not exist", type="warning")

        else:
            messages.add(u'Nothing to copy', type="info")

        self.request.response.redirect(context.absolute_url())
