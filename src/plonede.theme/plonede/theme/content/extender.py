from zope.component import adapts
from zope.interface import implements
from zope.component import getUtilitiesFor

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.Archetypes import atapi

from Products.Archetypes.public import ImageField
from Products.ATContentTypes.interface import IATFolder

from plonede.theme.browser.interfaces import IBanner

class BannerField(ExtensionField, ImageField):
   """A field that contains the styles."""
   
class ObjectExtender(object):
    adapts(IATFolder)
    implements(ISchemaExtender)

    fields = [BannerField('banner',
                     languageIndependent=False,
                     enforceVocabulary=False,
                     schemata='Banner',
                     widget = atapi.ImageWidget(label = u'Banner')
                     ),
    ]

    def __init__(self, context):
         self.context = context

    def getFields(self):
         return self.fields