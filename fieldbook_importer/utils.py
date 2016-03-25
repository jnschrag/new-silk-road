import datetime
from django.apps import apps
from django.utils.encoding import force_str
import re
from urllib.parse import urlparse

newlines_reg = re.compile("(\n|\r)")
extraspace_reg = re.compile("\s{2,}")


def get_mapper(mapping):
    def mapper(item):
        return {key: func(item) for key, func in mapping.items() if key and callable(func)}
    return mapper


def parse_date(date_str, fmt='%Y-%m-%d'):
    if not date_str:
        return None
    dt = datetime.datetime.strptime(date_str, fmt)
    return dt.date()


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


def instance_for_model(model_label, data):
    model = apps.get_model(model_label)
    try:
        instance = model.objects.get(**data)
    except model.DoesNotExist:
        instance = model(**data)
    except model.MultipleObjectsReturned as e:
        raise e
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


def make_url_list(list_str, sep=","):
    str_list = make_list(list_str, sep)
    if str_list:
        return [clean_url(x) for x in str_list if x]
    else:
        return None


def transform_attr(attr_name, func, *args, **kwargs):
    def inner_func(obj):
        attr_val = obj.get(attr_name, None) if obj else None
        if not func:
            return attr_val
        return func(attr_val, *args, **kwargs)
    return inner_func


def clean_string(value, stripnewlines=True):
    str_val = force_str(value).strip(" ")
    if stripnewlines:
        str_val = newlines_reg.sub(" ", str_val)
    str_val = extraspace_reg.sub(" ", str_val)
    return str_val


def force_split_string(value, sep=" "):
    if value and isinstance(value, str):
        return value.split(sep)
    return None


def section_from_string(value, pos, sep=" "):
    parts = force_split_string(value, sep)
    if parts and pos < len(parts):
        return parts[pos]
    return None


def remap_dict(obj, field_map):
    return {k: obj[v] for k, v in field_map.items() if v in obj}


def instances_for_related_items(items_list, model_label, field_map=None):
    if hasattr(items_list, '__iter__') or hasattr(items_list, '__next__'):
        for item in items_list:
            data = remap_dict(item, field_map) if field_map else item
            yield instance_for_model(model_label, data)
    else:
        return None


def first_of_many(many):
    if isinstance(many, list) and len(many) > 0:
        return many[0]
    elif hasattr(many, '__next__'):
        return next(many, None)
    return None
