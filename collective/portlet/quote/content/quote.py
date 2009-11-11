"""Definition of the Quote content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from collective.portlet.quote import RandomQuoteMessageFactory as _
from collective.portlet.quote.interfaces import IQuote
from collective.portlet.quote.config import PROJECTNAME

QuoteSchema = document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'source',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Source"),
            description=_(u"Who said it?"),
        ),
        required=True,
    ),
    
    atapi.StringField(
        'link',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Link"),
            description=_(u"A link to the quote"),
        ),
        validators=('isURL'),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

QuoteSchema['title'].storage = atapi.AnnotationStorage()
QuoteSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(QuoteSchema, moveDiscussion=False)

class Quote(document.ATDocumentBase):
    """Quote"""
    implements(IQuote)

    meta_type = "Quote"
    schema = QuoteSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    link = atapi.ATFieldProperty('link')

    source = atapi.ATFieldProperty('source')


atapi.registerType(Quote, PROJECTNAME)
