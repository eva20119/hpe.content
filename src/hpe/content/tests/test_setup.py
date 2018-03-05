# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from hpe.content.testing import HPE_CONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that hpe.content is properly installed."""

    layer = HPE_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if hpe.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'hpe.content'))

    def test_browserlayer(self):
        """Test that IHpeContentLayer is registered."""
        from hpe.content.interfaces import (
            IHpeContentLayer)
        from plone.browserlayer import utils
        self.assertIn(IHpeContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = HPE_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['hpe.content'])

    def test_product_uninstalled(self):
        """Test if hpe.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'hpe.content'))

    def test_browserlayer_removed(self):
        """Test that IHpeContentLayer is removed."""
        from hpe.content.interfaces import \
            IHpeContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(IHpeContentLayer, utils.registered_layers())
