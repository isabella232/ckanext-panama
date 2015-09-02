import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as lib_helpers

import ckanext.panama.helpers as panama_helpers

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
        return {
            'get_default_locale': panama_helpers.get_default_locale,
            'get_extra_exclude_fields':
                panama_helpers.get_extra_exclude_fields,
            'get_recently_updated_panama_datasets':
                panama_helpers.get_recently_updated_panama_datasets
        }

    # IPackageController

    def _fluent_to_core_fields(self, pkg_dict):
        '''Update the core field value in the pkg_dict with the mapped fluent
        field value in the current language, or of the default locale.'''

        # mapping between fluent field and core field
        fluent_core_field_map = [('fluent_title', 'title'),
                                 ('fluent_notes', 'notes'),
                                 ('fluent_name', 'name'),
                                 ('fluent_description', 'description')]

        def add_to_dict(dic, field_map):
            fluent_field = dic.get(field_map[0])
            if fluent_field and type(fluent_field) is dict:
                current_lang = lib_helpers.lang()
                if fluent_field.get(current_lang):
                    dic[field_map[1]] = fluent_field[current_lang]
                else:
                    dic[field_map[1]] = \
                        fluent_field[panama_helpers.get_default_locale()]
            return dic

        for field_map in fluent_core_field_map:
            # for packages
            add_to_dict(pkg_dict, field_map)

            # for resources
            if pkg_dict.get('resources'):
                for res_dict in pkg_dict['resources']:
                    add_to_dict(res_dict, field_map)

        return pkg_dict

    def before_index(self, pkg_dict):
        pkg_dict = self._fluent_to_core_fields(pkg_dict)
        log.info(pkg_dict)
        return pkg_dict

    def before_view(self, pkg_dict):
        return self._fluent_to_core_fields(pkg_dict)

    def after_show(self, context, pkg_dict):
        return self._fluent_to_core_fields(pkg_dict)
