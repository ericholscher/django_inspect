import django_filters
from django_inspect import base

class StandardApiFilter(django_filters.FilterSet):
    min_id = django_filters.CharFilter(name='pk', lookup_type='gt')
    max_id= django_filters.CharFilter(name='pk', lookup_type='lt')

def filter_for_model(model_class, field_list=[], api=False):
    ins = base.Inspecter(model_class)
    if api:
        base_filter = StandardApiFilter
    else:
        base_filter = django_filters.FilterSet
    class Filter(base_filter):
        if ins.title.field:
            title = django_filters.CharFilter(name=ins.title.field, lookup_type='contains')
            field_list.append('title')
        if ins.type.field:
            field_list.append(ins.type.field)
        if ins.tags.field:
            tags = django_filters.TagFilter(name=ins.tags.field)
        if ins.pub_date.field:
            pub_date = django_filters.DateRangeFilter(name=ins.pub_date.field)
            field_list.append('pub_date')
        if ins.content.field:
            content = django_filters.CharFilter(name=ins.content.field, lookup_type='contains')
            field_list.append('content')
        if ins.user.field:
            user = django_filters.CharFilter(name=ins.user.field + '__username')
            field_list.append('user')

        class Meta:
            model = model_class
            fields = field_list

    return Filter

