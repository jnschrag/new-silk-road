from django.apps import apps
from django.db import models
from django.core.exceptions import FieldDoesNotExist
from search.utils import doc_id_for_instance
from importlib import import_module


class ModelSerializer:
    class Meta:
        model = None
        fields = None
        doc_type = None

    def __init__(self):
        if not self.Meta.model:
            raise Exception('You must set a Meta class with a model attribute with a model label or class')
        if not self.Meta.fields:
            raise Exception('You must set a Meta class with a fields attribute with an iterable of field names')
        if not self.Meta.doc_type:
            raise Exception('You must set a Meta class with a doc_type attribute with a DocType model')

        self.model_class = apps.get_model(self.Meta.model) if isinstance(self.Meta.model, str) else self.Meta.model
        if not issubclass(self.model_class, models.Model):
            raise TypeError('model attribute must be a django Model subclass')

        if isinstance(self.Meta.doc_type, str):
            module_path, class_name = self.Meta.doc_type.rsplit('.', maxsplit=1)
            doctype_module = import_module(module_path)
            self._doc_type = getattr(doctype_module, class_name, None)
        else:
            self._doc_type = self.Meta.doc_type

        # TODO: Handle reverse_related fields that might be serialized
        self._field_names = set(self.Meta.fields)
        self._simple_field_names = set()
        self._choice_field_names = set()
        self._rel_field_names = set()
        self._attribute_field_map = {}

        model_fields = self.model_class._meta.get_fields()
        self._reverse_rel_field_names = [x.get_accessor_name() for x in model_fields if hasattr(x, 'get_accessor_name')]

        for field_name in self._field_names:
            field_getter_name = 'get_{}'.format(field_name)
            if field_name in self._reverse_rel_field_names:
                if hasattr(self, field_name):
                    self._rel_field_names.add(field_name)
                else:
                    raise AttributeError('If you supply the name of a relational (fk, m2m) field, you must also provide an attribute to define the mapping')
            elif hasattr(self, field_getter_name):
                func = getattr(self, field_getter_name)
                if not callable(func):
                    raise AttributeError('Serializer attributes starting with get_ must be methods (callable)')
                self._attribute_field_map[field_name] = field_getter_name
            else:
                field = self.model_class._meta.get_field(field_name)
                if hasattr(self, field_name):
                    # Use attribute definition to serialize
                    if field.is_relation:
                        self._rel_field_names.add(field_name)
                else:
                    if field.is_relation:
                        raise AttributeError((
                            str(field.name) +
                            ': If you supply the name of a relational (fk, m2m) field ' +
                            'you must also provide an attribute to define the mapping'
                        ))
                    if field.choices:
                        self._choice_field_names.add(field_name)
                    else:
                        self._simple_field_names.add(field_name)

    def serialize(self, instance):
        if not isinstance(instance, self.model_class):
            raise TypeError(str(self.__class__), 'Instance must match model class')

        obj_dict = {
            '_meta': {
                'id': instance.id,
                'model': instance._meta.object_name,
                'app': instance._meta.app_label,
            },
            '_id': doc_id_for_instance(instance),
        }

        for f in self._simple_field_names:
            try:
                field = self.model_class._meta.get_field(f)
                obj_dict[f] = field.value_from_object(instance)
            except FieldDoesNotExist:
                continue

        for f in self._rel_field_names:
            rel_map = getattr(self, f)
            rel_value = getattr(instance, f, None)
            if rel_value:
                obj_dict[f] = rel_map.serialize(rel_value.all() if rel_map.many else rel_value)

        for f in self._choice_field_names:
            get_display_value = getattr(instance, 'get_{}_display'.format(f), None)
            if get_display_value:
                obj_dict[f] = get_display_value()

        for field_name, field_func_name in self._attribute_field_map.items():
            func = getattr(self, field_func_name)
            obj_dict[field_name] = func(instance)

        return obj_dict

    @property
    def related_object_fields(self):
        return self._rel_field_names

    @property
    def doc_type(self):
        return self._doc_type

    def create_document(self, instance):
        obj_dict = self.serialize(instance)
        return self.doc_type(**obj_dict)


class RelatedSerializer:

    def __init__(self, mapping_class, many=False):
        if isinstance(mapping_class, str):
            module_path, class_name = self.Meta.doc_type.rsplit('.', maxsplit=1)
            module = import_module(module_path)
            mapping_class = getattr(module, class_name, None)
        if not issubclass(mapping_class, ModelSerializer):
            raise TypeError('RelatedSerializer requires a ModelSerializer subclass as the first argument')
        self.serializer = mapping_class()
        self.many = many

    def serialize(self, instance):
        if self.many:
            if isinstance(instance, models.Model):
                instance = [instance]
            return [self.serializer.serialize(item) for item in instance]
        else:
            return self.serializer.serialize(instance)
