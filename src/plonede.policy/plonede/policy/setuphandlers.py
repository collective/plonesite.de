from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES

def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('plonede.policy_various.txt') is None:
        return

    portal = context.getSite()
    # do stuff