import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as lib_helpers

from ckanext.panama.helpers import get_default_locale

import logging
log = logging.getLogger(__name__)


class PanamaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'panama')

    # ITemplateHelpers

    def get_helpers(self):
        return {'get_default_locale': get_default_locale}

    # IPackageController

    def _add_to_pkg_dict(self, pkg_dict):
        '''Ensure pkg_dict['title'] is set to the current lang if available,
        or default locale if not.'''
        fluent_title = pkg_dict.get('fluent_title')
        if fluent_title:
            current_lang = lib_helpers.lang()
            if fluent_title.get(current_lang):
                pkg_dict['title'] = fluent_title[current_lang]
            else:
                pkg_dict['title'] = \
                    fluent_title[get_default_locale()]

        return pkg_dict

    def before_view(self, pkg_dict):

        return self._add_to_pkg_dict(pkg_dict)

    def after_show(self, context, pkg_dict):

        return self._add_to_pkg_dict(pkg_dict)
