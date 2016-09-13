from pylons import config

from ckan.plugins import toolkit
from ckan.lib import search
from datetime import date, datetime, timedelta

import logging
log = logging.getLogger(__name__)


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

def panama_get_all_groups():

    groups = toolkit.get_action('group_list')(data_dict={
        'include_extras': True, 'all_fields': True
    })

    return groups
