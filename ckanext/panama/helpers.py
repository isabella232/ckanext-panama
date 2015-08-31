from pylons import config


def get_default_locale():
    return config.get('ckan.locale_default', 'en')


def get_extra_exclude_fields():
    return ['fluent_notes', 'fluent_title',
            'fluent_name', 'fluent_description']
