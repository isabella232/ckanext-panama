import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

# from ckanext.panama.validators import panama_fluent_text_output
from ckanext.panama.helpers import get_default_locale


class PanamaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    # plugins.implements(plugins.IValidators)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'panama')

    # # IValidators
    # def get_validators(self):
    #     return {'panama_text_output': panama_fluent_text_output}

    def get_helpers(self):
        return {'get_default_locale': get_default_locale}
