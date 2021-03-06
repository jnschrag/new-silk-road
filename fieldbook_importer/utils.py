import datetime
from django.apps import apps
from urllib.parse import urlparse


def parse_date(date_str, fmt='%Y-%m-%d'):
    if not date_str or not isinstance(date_str, str):
        return None
    try:
        dt = datetime.datetime.strptime(date_str, fmt)
        return dt.date()
    except ValueError:
        return None


def values_list(l, field_name, default=None):
    if l:
        for i in l:
            yield i.get(field_name, default)
    return None


def find_choice(search_str, choices):
    if not search_str:
        return None
    result = list(value for value, name in choices if name.lower() == search_str.lower())
    if len(result) == 1:
        return result[0]
    else:
        return None


def choices_from_values(values, choices):
    for v in values:
        yield find_choice(v, choices)


# TODO: Handle invalid data, like None for required field
def instance_for_model(model_label, data, create=False, skiperrors=False):
    model = apps.get_model(model_label)
    if create:
        try:
            instance, created = model.objects.get_or_create(**data)
        except TypeError as e:
            if skiperrors:
                return None
            raise e
    else:
        try:
            instance = model.objects.get(**data)
        except model.DoesNotExist:
            instance = None
        except model.MultipleObjectsReturned as e:
            raise e
            if skiperrors:
                return None
    return instance


def make_list(list_str, sep=","):
    if not list_str:
        return None
    return [s.strip() for s in list_str.split(sep)]


def clean_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://{}".format(url)
    return url


def make_url_list(list_str, sep=", "):
    str_list = make_list(list_str, sep)
    if str_list:
        return [clean_url(x) for x in str_list if x and x[0].isalnum()]
    else:
        return None


def force_split_string(value, sep=" "):
    if isinstance(value, str):
        return value.split(sep)
    return None


def section_from_string(value, pos, sep=" "):
    parts = force_split_string(value, sep)
    if parts and pos < len(parts):
        return parts[pos]
    return None


def remap_dict(obj, field_map):
    return {
        k: v(obj)
        if callable(v) else obj.get(v, None)
        for k, v in field_map.items()
    }


def instances_for_related_items(items_list, model_label, transformer=None, create=False):
    if hasattr(items_list, '__iter__') or hasattr(items_list, '__next__'):
        for item in items_list:
            data = transformer(item) if callable(transformer) else item
            try:
                yield instance_for_model(model_label, data, create=create)
            except Exception:
                pass
    else:
        return None


def instances_or_none(in_var, model_name, transformer=None):
    if in_var:
        return list(instances_for_related_items(
            in_var,
            model_name,
            transformer
        ))
    return None


def first_of_many(many):
    if isinstance(many, list) and len(many) > 0:
        return many[0]
    elif hasattr(many, '__next__'):
        return next(many, None)
    return None


def coerce_to_boolean_or_null(value):
    if isinstance(value, str):
        normalized_val = value.lower().strip()
        if normalized_val == 'yes':
            return True
        elif normalized_val == 'no':
            return False
    elif isinstance(value, bool):
        return value
    return None


def first_value_or_none(value):
    if isinstance(value, list) and len(value) > 0:
        return value[0]
    return None


def parse_int(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    return None
