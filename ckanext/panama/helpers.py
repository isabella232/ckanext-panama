import logging
from datetime import datetime

from ckan import logic
from ckan.lib import search
from ckan.plugins import toolkit
from pylons import config

log = logging.getLogger(__name__)


def get_default_locale():
    return config.get('ckan.locale_default', 'en')


def get_extra_exclude_fields():
    return ['fluent_notes', 'fluent_title', 'fluent_name', 'fluent_description']


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
            package = toolkit.get_action('package_show')(data_dict={'id': pkg['id']})
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


def panama_get_featured_groups(count=1):
    '''Returns a list of favourite group the form
    of organization_list action function
    '''
    config_groups = config.get('ckan.featured_groups', '').split()
    groups = featured_group_org(get_action='group_show', list_action='group_list', count=count, items=config_groups)
    return groups


def featured_group_org(items, get_action, list_action, count):
    def get_group(id):
        context = {'ignore_auth': True, 'limits': {'packages': 2}, 'for_view': True}
        data_dict = {'id': id, 'include_datasets': False, 'include_users': False}

        try:
            out = logic.get_action(get_action)(context, data_dict)
        except logic.NotFound:
            return None
        return out

    groups_data = []

    extras = logic.get_action(list_action)({}, {})

    # list of found ids to prevent duplicates
    found = []
    for group_name in items + extras:
        group = get_group(group_name)
        if not group:
            continue
        # check if duplicate
        if group['id'] in found:
            continue
        found.append(group['id'])
        groups_data.append(group)
        if len(groups_data) == count:
            break

    return groups_data
