import random
from zope.interface import implements
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from collective.portlet.quote import RandomQuoteMessageFactory as _


class IRandomQuote(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    title = schema.TextLine(
        title=_(u"Portlet title"),
        description=_(u"Portlet title"),
        required=False)
    
    target_folder = schema.Choice(
        title=_(u"Quote folder"),
        description=_(u"The folder that has the quotes in it"),
        required=True,
        source=SearchableTextSourceBinder({'is_folderish' : True}),
        )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IRandomQuote)

    title = u"Random Quote"

    def __init__(self, title=u"", target_folder=None):
        self.title = title
        self.target_folder = target_folder
        

class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('randomquote.pt')
    _quote = None
    
    def _find_quote(self):
        if self._quote is not None:
            return self._quote
        
        catalog = self.context.portal_catalog
        brains = catalog(path=self.data.target_folder, portal_type="Quote")
        if not brains:
            return None
        self._quote = random.choice(brains).getObject()
        return self._quote
        
    def get_quote(self):
        quote = self._find_quote()
        if quote is None:
            return ""
        return quote.getText()
        
    def get_source(self):
        quote = self._find_quote()
        if quote is None:
            return ""
        return quote.getSource()

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRandomQuote)
    form_fields['target_folder'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IRandomQuote)
    form_fields['target_folder'].custom_widget = UberSelectionWidget
