from ckan.common import OrderedDict
from pylons import config
from ckan.plugins import toolkit
import ckanapi


groups = OrderedDict([
    ('local-governments', 'Local Governments'),
    ('health', 'Health'),
    ('business', 'Business'),
    ('transportation', 'Transportation'),
    ('education', 'Education'),
    ('justice', 'Justice'),
    ('social-development', 'Social Development'),
    ('finance', 'Finance'),
    ('labour', 'Labour'),
    ('environment', 'Environment'),
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

        for name, title in groups.items():
            try:
                result = local_ckan.action.group_create(
                    name=name,
                    title=title,
                    image_url='{url}/images/{image}.png'.format(url=url,
                                                                image=name)
                )
                print result
            except ckanapi.ValidationError, e:
                print e
