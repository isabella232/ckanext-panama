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
        '''Ensure pkg_dict[<core field>] is set to the current lang if
        available, or default locale if not.'''

        # mapping between fluent field and core field
        fluent_core_field_map = [('fluent_title', 'title'),
                                 ('fluent_notes', 'notes')]

        for field_map in fluent_core_field_map:
            fluent_field = pkg_dict.get(field_map[0])
            if fluent_field:
                current_lang = lib_helpers.lang()
                if fluent_field.get(current_lang):
                    pkg_dict[field_map[1]] = fluent_field[current_lang]
                else:
                    pkg_dict[field_map[1]] = \
                        fluent_field[get_default_locale()]

        return pkg_dict

    def before_view(self, pkg_dict):

        return self._add_to_pkg_dict(pkg_dict)

    def after_show(self, context, pkg_dict):

        return self._add_to_pkg_dict(pkg_dict)
