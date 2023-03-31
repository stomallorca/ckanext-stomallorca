import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckan.common import config
from ckan.model import Package
import ckan.lib.helpers as h

def default_locale():
    '''Wrap the ckan default locale in a helper function to access
    in templates.
    Returns 'en' by default.
    :rtype: string
    '''
    value = config.get('ckan.locale_default', 'en')
    return value

def stomallorca_portal_url():
    portal_url = config.get('ckanext.stomallorca_theme.portal_url', 'https://stomallorca.com/')
    if (h.lang() != 'es'):
      portal_url += h.lang() + '/'
    return portal_url

def remove_html_tags(html):
    return ''.join(xml.etree.ElementTree.fromstring(html).itertext())

def get_license(license_id):
    '''Helper to return license based on id.
    '''
    return Package.get_license_register().get(license_id)

def get_group(group_id):
    '''Helper to return the group.
    CKAN core has a get_organization helper but does not have one for groups.
    This also allows us to access the group with all extras which are needed to 
    access the scheming/fluent fields.
    '''
    group_dict = toolkit.get_action('group_show')(
        data_dict={'id': group_id})
    return group_dict

class StomallorcaThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "stomallorca_theme")

    # ITemplateHelpers
    def get_helpers(self):
        """
        Provide template helper functions
        """
        return {
            'extrafields_default_locale': default_locale,
            'stomallorca_portal_url': stomallorca_portal_url,
            'stomallorca_theme_get_license': get_license,
            'stomallorca_theme_get_group': get_group,
        }

    # IPackageController
    def before_dataset_search(self, search_params):
        search_params['q'] = search_params.get('q', '').lower()
        return search_params

