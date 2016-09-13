from pylons import config

from ckan.plugins import toolkit
from ckan.lib import search
from datetime import date, datetime, timedelta
import ckan.lib.helpers as lib_helpers

import logging
log = logging.getLogger(__name__)


def _fluent_to_core_fields(dic, fluent_core_field_map):
    '''Update the core field value in the dic with the mapped fluent
    field value in the current language, or of the default locale.'''

    def add_to_dict(d, field_map):
        fluent_field = d.get(field_map[0])
        if fluent_field and type(fluent_field) is dict:
            current_lang = lib_helpers.lang()
            if fluent_field.get(current_lang):
                d[field_map[1]] = fluent_field[current_lang]
            else:
                d[field_map[1]] = \
                    fluent_field[get_default_locale()]
        return d

    for field_map in fluent_core_field_map:
        # for packages and groups
        add_to_dict(dic, field_map)

        # for resources (if present)
        if dic.get('resources'):
            for res_dict in dic['resources']:
                add_to_dict(res_dict, field_map)

    return dic

def get_default_locale():
    return config.get('ckan.locale_default', 'en')


def get_extra_exclude_fields():
    return ['fluent_notes', 'fluent_title',
            'fluent_name', 'fluent_description']


def get_recently_updated_panama_datasets(limit=3):
    try:
        pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'metadata_modified desc',
            'rows': limit,
        })['results']

    except toolkit.ValidationError, search.SearchError:
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(data_dict={
                'id': pkg['id']
            })
            modified = datetime.strptime(package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['days_ago_modified'] = ((datetime.now() - modified).days)
            pkgs.append(package)
        return pkgs

def panama_get_group_fluent_name(group):
    group = toolkit.get_action('group_show')(data_dict={'id': group})
    # TODO: This shouldn't be hardcoded, find why h.lang() doesn't return any value
    try:
        fluent_title = group['fluent_title']['es']
    except KeyError:
        fluent_title = group['name']

    return fluent_title

def panama_get_groups_len():

    groups = toolkit.get_action('group_list')(data_dict={})
    groups_len = len(groups)

    return groups_len
