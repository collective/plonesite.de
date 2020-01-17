# -*- coding: utf-8 -*-
from plone import api
from zExceptions import BadRequest
from zope.lifecycleevent import modified
from zope.globalrequest import getRequest

import logging
import transaction

log = logging.getLogger(__name__)


def cleanup(context=None):
    remove_overrides()
    release_all_webdav_locks()
    remove_all_revisions()
    disable_theme()


def remove_overrides(context=None):
    log.info('removing portal_skins overrides')
    portal_skins = api.portal.get_tool('portal_skins')
    custom = portal_skins['custom']
    for name in custom.keys():
        custom.manage_delObjects([name])
        log.info(u'Removed skin item {}'.format(name))

    log.info('removing portal_view_customizations')
    view_customizations = api.portal.get_tool('portal_view_customizations')
    for name in view_customizations.keys():
        view_customizations.manage_delObjects([name])
        log.info(u'Removed portal_view_customizations item {}'.format(name))


def release_all_webdav_locks(context=None):
    from Products.CMFPlone.utils import base_hasattr
    portal = api.portal.get()

    def unlock(obj, path):
        if base_hasattr(obj, 'wl_isLocked') and obj.wl_isLocked():
            obj.wl_clearLocks()
            log.info(u'Unlocked {}'.format(path))

    portal.ZopeFindAndApply(portal, search_sub=True, apply_func=unlock)



def remove_all_revisions(context=None):
    """Remove all revisions.
    After packing the DB this could significantly shrink its size.
    """
    hs = api.portal.get_tool('portal_historiesstorage')
    zvcr = hs.zvc_repo
    zvcr._histories.clear()
    storage = hs._shadowStorage
    storage._storage.clear()



def disable_theme(context=None):
    """Disable a custom diazo theme and enable sunburst.
    Useful for cleaning up a site in Plone 4
    """
    THEME_NAME = 'plonede.theme'
    from plone.app.theming.utils import applyTheme
    portal_skins = api.portal.get_tool('portal_skins')
    qi = api.portal.get_tool('portal_quickinstaller')
    if qi.isProductInstalled(THEME_NAME):
        log.info('Uninstalling {}'.format(THEME_NAME))
        qi.uninstallProducts([THEME_NAME])
    log.info('Disabling all diazo themes')
    applyTheme(None)
    log.info('Enabled Sunburst Theme')
    portal_skins.default_skin = 'Sunburst Theme'
    if 'Plone.de Theme' in portal_skins.getSkinSelections():
        portal_skins.manage_skinLayers(['Plone.de Theme'], del_skin=True)


def remove_addons(context=None):
    remove_ploneformgen()
    qi = api.portal.get_tool('portal_quickinstaller')
    portal_properties = api.portal.get_tool('portal_properties')
    portal_setup = api.portal.get_tool('portal_setup')
    portal_catalog = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()
    portal_controlpanel = api.portal.get_tool('portal_controlpanel')

    # quintagroup.plonecaptchas
    log.info('removing quintagroup.plonecaptchas')
    if qi.isProductInstalled('quintagroup.plonecaptchas'):
        qi.uninstallProducts(['quintagroup.plonecaptchas'])

    log.info('removing quintagroup.captcha.core')
    if qi.isProductInstalled('quintagroup.captcha.core'):
        qi.uninstallProducts(['quintagroup.captcha.core'])

    log.info('removing quintagroup.formlib.captcha')
    if qi.isProductInstalled('quintagroup.formlib.captcha'):
        qi.uninstallProducts(['quintagroup.formlib.captcha'])

    log.info('removing quintagroup.z3cform.captcha')
    if qi.isProductInstalled('quintagroup.z3cform.captcha'):
        qi.uninstallProducts(['quintagroup.z3cform.captcha'])

    log.info('removing collective.sponsor')
    if qi.isProductInstalled('collective.sponsor'):
        qi.uninstallProducts(['collective.sponsor'])

    log.info('removing wpd.countdown')
    if qi.isProductInstalled('wpd.countdown'):
        qi.uninstallProducts(['wpd.countdown'])

    log.info('removing collective.portlet.feedmixer')
    if qi.isProductInstalled('collective.portlet.feedmixer'):
        qi.uninstallProducts(['collective.portlet.feedmixer'])

    log.info('removing Products.Maps')
    if qi.isProductInstalled('Products.Maps'):
        qi.uninstallProducts(['Products.Maps'])
    try:
        portal.portal_properties.manage_delObjects(['maps_properties'])
    except BadRequest:
        pass


def remove_ploneformgen(context=None):
    portal = api.portal.get()
    portal_types = api.portal.get_tool('portal_types')
    portal_catalog = api.portal.get_tool('portal_catalog')
    qi = api.portal.get_tool('portal_quickinstaller')

    log.info('removing PloneFormGen')
    old_types = [
        'FormFolder',
    ]
    old_types = [i for i in old_types if i in portal_types]
    for old_type in old_types:
        for brain in portal_catalog(portal_type=old_type):
            log.info(u'Deleting Existing Instances of {}!'.format(old_type))
            api.content.delete(brain.getObject(), check_linkintegrity=True)
    try:
        portal.manage_delObjects(['formgen_tool'])
    except AttributeError:
        pass
    try:
        portal.portal_properties.manage_delObjects(['ploneformgen_properties'])
    except BadRequest:
        pass

    if qi.isProductInstalled('PloneFormGen'):
        qi.uninstallProducts(['PloneFormGen'])

    if qi.isProductInstalled('Products.PloneFormGen'):
        qi.uninstallProducts(['Products.PloneFormGen'])


def cleanup_in_plone52(context=None):
    migrate_ATBTreeFolder()
    uninstall_archetypes()
    remove_archetypes_traces()


def migrate_ATBTreeFolder(context=None):
    """Replace very old containers for news, events and Members
    """
    from plone.portlets.interfaces import ILocalPortletAssignmentManager
    from plone.portlets.interfaces import IPortletManager
    from zope.component import getMultiAdapter
    from zope.component import queryUtility

    portal = api.portal.get()
    # create new containers:
    if not portal['Members'].__class__.__name__ == 'ATBTreeFolder':
        log.info('Migrating ATBTreeFolder not needed')
        return
    log.info('Migrating ATBTreeFolders')
    members_new = api.content.create(
      container=portal,
      type='Folder',
      id='members_new',
      title=u'Benutzer',
    )
    members_new.setOrdering('unordered')
    members_new.setLayout('@@member-search')
    # Block all right column portlets by default
    manager = queryUtility(IPortletManager, name='plone.rightcolumn')
    if manager is not None:
        assignable = getMultiAdapter(
            (members_new, manager),
            ILocalPortletAssignmentManager
        )
        assignable.setBlacklistStatus('context', True)
        assignable.setBlacklistStatus('group', True)
        assignable.setBlacklistStatus('content_type', True)


    for item in portal.Members.contentValues():
        api.content.move(
            source=item,
            target=members_new,
            )
    api.content.delete(obj=portal['Members'], check_linkintegrity=False)
    api.content.rename(obj=portal['members_new'], new_id='Members')


def uninstall_archetypes(context=None):
    portal = api.portal.get()
    request = getRequest()
    installer = api.content.get_view('installer', portal, request)
    addons = [
        'Archtypes',
        'ATContentTypes',
        'plone.app.referenceablebehavior',
        'plone.app.blob',
        'plone.app.imaging',
    ]
    for addon in addons:
        if installer.is_product_installed(addon):
            installer.uninstall_product(addon)


def remove_archetypes_traces(context=None):
    portal = api.portal.get()

    # remove obsolete AT tools
    tools = [
        'portal_languages',
        'portal_tinymce',
        'kupu_library_tool',
        'portal_factory',
        'portal_atct',
        'uid_catalog',
        'archetype_tool',
        'reference_catalog',
        'portal_metadata',
    ]
    for tool in tools:
        if tool not in portal.keys():
            log.info('Tool {} not found'.format(tool))
            continue
        try:
            portal.manage_delObjects([tool])
            log.info('Deleted {}'.format(tool))
        except Exception as e:
            log.info(u'Problem removing {}: {}'.format(tool, e))
            try:
                log.info(u'Fallback to remove without permission_checks')
                portal._delObject(tool)
                log.info('Deleted {}'.format(tool))
            except Exception as e:
                log.info(u'Another problem removing {}: {}'.format(tool, e))
