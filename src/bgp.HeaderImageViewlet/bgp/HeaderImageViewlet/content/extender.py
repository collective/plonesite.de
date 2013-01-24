from Products.Archetypes.public import ImageField
from archetypes.schemaextender.field import ExtensionField

from zope.component import adapts
from zope.interface import implements
from zope.component import getUtilitiesFor
from bgp.HeaderImageViewlet.browser.interfaces import IHeaderImage
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.ATContentTypes.interface import IATFolder
from Products.Archetypes.public import ImageField

class HeaderImageField(ExtensionField, ImageField):
   """A field that contains the styles."""
   
class ObjectExtender(object):
    adapts(IATFolder)
    implements(ISchemaExtender)

    fields = [
            HeaderImageField('headerimage',
                            languageIndependent=False,
                            enforceVocabulary=False,
	                    schemata='HeaderImage',
		  ),
    ]

    def __init__(self, context):
         self.context = context

    def getFields(self):
         return self.fields
