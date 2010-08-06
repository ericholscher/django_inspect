from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from utils import get_field_by_type, get_related_field

class Inspecter(object):
    """
    The actual class you use, which basically just maps a bunch of parsers
    """

    def __init__(self, model=None, mapping=None):
        self.parsers = {}
        self.model = model
        for parser in BaseParser.__subclasses__():
            active = getattr(parser, 'active', True)
            if active:
                self.parsers[parser.key] = parser(model, mapping=mapping)
                setattr(self.__class__, parser.key, parser(model, mapping=mapping))

class BaseParser(object):
    """
    Handle any mapping passed in.
    All parsers should subclass this.
    """

    def __get__(self, instance, owner):
        self._instance = instance
        self._parsers = instance.parsers
        return self

    def __init__(self, model, mapping=None):
        self.model = model
        self.app_string = "%s.%s" % (model._meta.app_label, model._meta.module_name)
        if mapping:
            self.mapping = mapping
        else:
            self.mapping = getattr(settings, 'INSPECT_MAPPINGS', None)


    @property
    def field(self):
        if self.mapping and self.mapping.has_key(self.app_string):
            return self.mapping[self.app_string][self.key]
        elif hasattr(self.model, self.key):
            return self.key
        return None

    @property
    def value(self):
        if not self.field:
            return None
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

class PointParser(BaseParser):
    key = 'point'

    @property
    def field(self):
        field = super(PointParser, self).field
        if self._parsers.has_key('latitude') and self._parsers.has_key('longitude'):
            return (self._instance.latitude.field, self._instance.longitude.field)
        if field:
            return field
        if hasattr(self.model, 'lat'):
            return 'lat'
        return None

class LatParser(BaseParser):
    key = 'latitude'

    @property
    def field(self):
        field = super(LatParser, self).field
        if field:
            return field
        if hasattr(self.model, 'lat'):
            return 'lat'
        return None

class LongParser(BaseParser):
    key = 'longitude'

    @property
    def field(self):
        field = super(LongParser, self).field
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

class NameParser(BaseParser):
    key = 'name'

class TagParser(BaseParser):
    key = 'tags'

class AddressParser(BaseParser):
    key = 'address'

    @property
    def field(self):
        field = super(AddressParser, self).field
        if field:
            return field
        if hasattr(self.model, 'address1'):
            return 'address1'
        return None

class PhoneParser(BaseParser):
    key = 'phone'

    @property
    def field(self):
        field = super(PhoneParser, self).field
        if field:
            return field
        if hasattr(self.model, 'phone1'):
            return 'phone1'
        return None

class TypeParser(BaseParser):
    key = 'type'

    @property
    def field(self):
        field = super(TypeParser, self).field
        if field:
            return field
        if hasattr(self.model, 'activity_type'):
            return 'activity_type'
        if hasattr(self.model, 'notice_type'):
            return 'notice_type'
        return None

