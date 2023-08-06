# -*- coding: utf-8 -*-
from acentoweb.collectionactions.behaviors.collection_copy import ICollectionCopyMarker
from acentoweb.collectionactions.testing import ACENTOWEB_COLLECTIONACTIONS_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class CollectionCopyIntegrationTest(unittest.TestCase):

    layer = ACENTOWEB_COLLECTIONACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_collection_copy(self):
        behavior = getUtility(IBehavior, 'acentoweb.collectionactions.collection_copy')
        self.assertEqual(
            behavior.marker,
            ICollectionCopyMarker,
        )
