from pylons import config


def get_default_locale():
    return config.get('ckan.locale_default', 'en')
