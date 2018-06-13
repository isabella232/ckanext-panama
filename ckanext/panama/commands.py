# -*- coding: utf-8 -*-

from ckan.common import OrderedDict
from pylons import config
from ckan.plugins import toolkit
import ckanapi


groups = OrderedDict([
    ('governments', ('Gobiernos Locales', 'Local Governments')),
    ('health', ('Salud', 'Health')),
    ('business', ('Comercio e Industrias', 'Business')),
    ('transportation', ('Transporte y Logística', 'Transportation')),
    ('education', ('Educación', 'Education')),
    ('justice', ('Justicia', 'Justice')),
    ('social-development', ('Desarrollo Social', 'Social Development')),
    ('environment', ('Ambiente', 'Environment')),
    ('agricultural', ('Agropecuario y Pesca', 'Agriculture and Fisheries')),
    ('territory', ('Ordenamiento Territorial', 'Land Use')),
    ('security', ('Orden Publico y Seguridad', 'Public Order and Security')),
    ('tourism', ('Turismo', 'Tourism'))
])


class CreateFeaturedGroups(toolkit.CkanCommand):
    '''Create featured groups

    Usage:
      create_featured_groups             - create featured groups
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0

    def command(self):
        self._load_config()

        url = config['ckan.site_url']
        local_ckan = ckanapi.LocalCKAN()

        print groups.items

        for name, title in groups.items():
            try:
                result = local_ckan.action.group_create(
                    name=name,
                    display_name=title,
                    image_url='{url}/images/{image}.png'.format(url=url,
                                                                image=name)
                )
                print result
            except ckanapi.ValidationError, e:
                print e
