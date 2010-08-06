
def get_field_by_type(model, field_type):
    found = []
    for f in model._meta.fields + model._meta.many_to_many:
        if isinstance(f, field_type):
            found.append(f)
    if not found:
        return None
    if len(found) > 1:
        #Handle this gracefully.
        #raise TypeError('Expected only one field of this type.')
        pass
    return found[0].name

def get_related_field(model, related_model):
    for f in model._meta.fields + model._meta.many_to_many:
        if f.rel and f.rel.to == related_model:
            return f.name
    return None
