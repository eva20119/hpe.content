from hpe.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.vocabularies.catalog import CatalogSource
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource


class IHpeContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IBicyclePicture(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )
    event = RelationChoice(
        title=_(u'Event Select'),
        source=CatalogSource(Type="EventList"),
        required=False,
    )
    place = RelationChoice(
        title=_(u'Place Select'),
        source=CatalogSource(Type="PlaceList"),
        required=False,
    )
    image = NamedBlobImage(
        title=_(u"Upload Image"),
        required=False
    )


class IEventList(Interface):
    title = schema.TextLine(
        title=_(u'Event'),
        required=True,
    )


class IPlaceList(Interface):
    title = schema.TextLine(
        title=_(u'Place'),
        required=True,
    )


class IReservation(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=False
    )
    date = schema.Datetime(
        title=_(u'Reservation Date Time'),
        required=False
    )
    peroid1 = schema.TextLine(
        title=_(u'Peroid1 Reservation Name'),
        required=False,
    )
    peroid2 = schema.TextLine(
        title=_(u'Peroid2 Reservation Name'),
        required=False,
    )
    peroid3 = schema.TextLine(
        title=_(u'Peroid3 Reservation Name'),
        required=False,
    )
    peroid4 = schema.TextLine(
        title=_(u'Peroid4 Reservation Name'),
        required=False,
    )
    peroid5 = schema.TextLine(
        title=_(u'Peroid5 Reservation Name'),
        required=False,
    )
    peroid6 = schema.TextLine(
        title=_(u'Peroid6 Reservation Name'),
        required=False,
    )
    alternate = schema.Text(
        title=_(u'Alternate Name'),
        required=False,
    )
