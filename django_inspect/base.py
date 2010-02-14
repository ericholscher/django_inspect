from django.db import models
from django.contrib.auth.models import User

from utils import get_field_by_type, get_related_field

class Inspecter(object):
    """
    The actual class you use, which basically just maps a bunch of parsers
    """

    def __init__(self, model=None, mapping=None):
        self.model = model
        for parser in BaseParser.__subclasses__():
            active = getattr(parser, 'active', True)
            if active:
                setattr(self, parser.key, parser(model, mapping=mapping))


class BaseParser(object):
    """
    Handle any mapping passed in.
    All parsers should subclass this.
    """

    def __init__(self, model, mapping=None):
        self.model = model
        self.app_string = "%s.%s" % (model._meta.app_label, model._meta.module_name)
        self.mapping = mapping

    @property
    def field(self):
        if self.mapping and self.mapping.has_key(self.app_string):
            return self.mapping[self.app_string][self.key]
        elif hasattr(self.model, self.key):
            return self.key
        return None

    @property
    def value(self):
        return getattr(self.model, self.field)

class ContentParser(BaseParser):
    key = 'content'

    @property
    def field(self):
        field = super(ContentParser, self).field
        if field:
            return field
        if hasattr(self.model, 'comment'):
            return 'comment'
        return get_field_by_type(self.model, models.TextField)

class PubDateParser(BaseParser):
    key = 'pub_date'

    @property
    def field(self):
        field = super(PubDateParser, self).field
        if field:
            return field
        if hasattr(self.model, 'submit_date'):
            return 'submit_date'
        return get_field_by_type(self.model, models.DateTimeField)

class TitleParser(BaseParser):
    key = 'title'

class IpAddressParser(BaseParser):
    key = 'ip_address'

class LatParser(BaseParser):
    key = 'latitude'

    @property
    def field(self):
        field = super(PubDateParser, self).field
        if field:
            return field
        if hasattr(self.model, 'lat'):
            return 'lat'
        return None

class LongParser(BaseParser):
    key = 'longitude'

    @property
    def field(self):
        field = super(PubDateParser, self).field
        if field:
            return field
        if hasattr(self.model, 'long'):
            return 'long'
        return None

class UserParser(BaseParser):
    key = 'user'

    @property
    def field(self):
        field = super(UserParser, self).field
        if field:
            return field
        if hasattr(self.model, 'author'):
            return 'author'
        return get_related_field(self.model, User)