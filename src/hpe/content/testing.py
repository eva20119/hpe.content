# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import hpe.content


class HpeContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=hpe.content)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'hpe.content:default')


HPE_CONTENT_FIXTURE = HpeContentLayer()


HPE_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(HPE_CONTENT_FIXTURE,),
    name='HpeContentLayer:IntegrationTesting'
)


HPE_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(HPE_CONTENT_FIXTURE,),
    name='HpeContentLayer:FunctionalTesting'
)


HPE_CONTENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        HPE_CONTENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='HpeContentLayer:AcceptanceTesting'
)
