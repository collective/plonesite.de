from Products.CMFCore.utils import getToolByName
from plonede.content.config import PROJECTNAME
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
from Products.CMFPlone.interfaces import IPropertiesTool

# maybe we use this later on
#_PROPERTIES = [
#    dict(name='prop', type_='string', value='val'),
#]

def setupVarious(context):

    if context.readDataFile('plonede.content_various.txt') is None:
        return
    
    site = context.getSite()
    logger = context.getLogger(PROJECTNAME)

    #setVersionedTypes(site)
    #add_catalog_indexes(site, logger)
    #setProperties(site)


def setProperties(site):
    """Enable versioning for custom content types used by iterate
    """
    properties_tool = getToolByName(site, 'portal_properties')
    properties = properties_tool.plonede_properties

    for property in _PROPERTIES:
        if not properties.hasProperty(property['name']):
            properties.manage_addProperty(property['name'], property['value'], property['type_'])
    

def setVersionedTypes(site):
    """Enable versioning for custom content types used by iterate
    """
    
    portal_repository = getToolByName(site, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in ('Content Type', ):
        if type_id not in versionable_types:
            versionable_types.append(type_id)
            # Add default versioning policies to the versioned type
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)


def add_catalog_indexes(site, logger):
    """Add our indexes to the catalog.

    Doing it here instead of in profiles/default/catalog.xml means we
    do not need to reindex those indexes after every reinstall.
    """
    catalog = getToolByName(site, 'portal_catalog')
    indexes = catalog.indexes()

    wanted = (("fieldname", "FieldIndex"),
             )
    
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            logger.info("Added %s for field %s.", meta_type, name)
            
        if name not in catalog.schema():
            catalog.addColumn(name)
            logger.info("Added Column for %s.", name)