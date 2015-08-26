import json

import ckan.lib.helpers as lib_helpers

import logging
log = logging.getLogger(__name__)


def panama_fluent_text_output(value):
    '''
    Return stored json representation as a single string value based on the
    selected locale. If value is already a string just pass it through.
    '''
    lang = lib_helpers.lang()
    log.info(lang)
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value)
    except ValueError:
        # plain string in the db, just return it
        return value
