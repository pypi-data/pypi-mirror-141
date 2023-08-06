from typing import (
    Any,
    Callable,
    Dict,
    List,
    Union,
)

from django.apps import apps
from django.db import transaction
from django.db.models import Model
from django.db.models.fields.related import (
    RelatedField,
    ManyToManyField,
)
from django.db.models.fields.reverse_related import (
    ForeignObjectRel,
    ManyToManyRel,
)

from .exceptions import NotAllRelatedInstancesSaved


class OverrideFieldDict(dict):
    pass


class CallableValue:
    """
    Wrap your callable in this class when you override field.
    It prevents from unwanted calls.
    """
    def __init__(self, get_value: Callable):
        self.get_value = get_value

    def __call__(self, instance: Model) -> Any:
        return self.get_value(instance)


@transaction.atomic
def duplicate(instance, override_fields: Union[OverrideFieldDict, dict] = None, paths: List[str] = None):
    """Create a copy of model instance with related objects (deep or single level depending on deep argument).

    :param instance: a copied model instance
    :param override_fields: override instance files with given values
    :param paths: a list of relation paths to copy in duplication process
    :return: new instance
    """
    override_fields = override_fields or OverrideFieldDict()
    paths = paths or []

    duplicate_object = instance.duplicate_class(
        instance,
        override_fields=dictify_override_fields(override_fields),
        paths_graph=dictify_paths_list(paths),
    )
    new_instance = duplicate_object.save()
    check_if_all_instances_were_saved(duplicate_object)
    return new_instance


def load_models_from_str(models):
    """Return list of models passed as strings"""

    loaded_models = []
    for model in models:
        loaded_models.append(load_model_from_str(model))
    return loaded_models


def load_model_from_str(model):
    if isinstance(model, str):
        return apps.get_model(*model.split('.'))
    return model


def check_if_all_instances_were_saved(duplicate_object):
    if any(obj.new_instance.pk is None for obj in duplicate_object.memo.values()):
        raise NotAllRelatedInstancesSaved(duplicate_object)


def dictify_override_fields(override_fields: Dict[str, Any]) -> dict:
    """Makes nested dict from nested dotted strings

    >>> dictify_override_fields({'x.y.z': 1, 'x.y.v': 2})
    {'x': {'y': {'z': 1, 'v': 2}}}
    """

    override_fields_dict = OverrideFieldDict()
    for nested_override_field, value in override_fields.items():
        most_nested_dict = override_fields_dict
        fields_path = nested_override_field.split('.')
        for field_name in fields_path[:-1]:
            most_nested_dict = most_nested_dict.setdefault(field_name, OverrideFieldDict())
        most_nested_field_name = fields_path[-1]
        most_nested_dict[most_nested_field_name] = value
    return override_fields_dict


def dictify_paths_list(paths_list):
    path_dict = {}
    for path in paths_list:
        if '.' in path:
            part, rest = path.split('.', 1)
            path_dict.setdefault(part, []).append(rest)
        else:
            path_dict.setdefault(path, [])
    for path, nested_paths in path_dict.items():
        path_dict[path] = dictify_paths_list(nested_paths)
    return path_dict


def generate_known_relations_dict():
    from .models import DuplicateMixin
    relations_dict = {}
    for model in apps.get_models():
        if issubclass(model, DuplicateMixin):
            fill_relations_dict(model, relations_dict)
    return relations_dict


def fill_relations_dict(model, result_dict):
    to_process = [model]

    while to_process:
        current_model = to_process.pop()
        collect_models_relations(current_model, to_process, result_dict)

    return result_dict


def collect_models_relations(model, to_process, result_dict):
    relation_list = result_dict[model_label(model)] = []

    for field in model._meta.get_fields():
        if isinstance(field, ManyToManyField):
            relation_list.append(field.name)
            next_model = field.remote_field.through
        elif isinstance(field, RelatedField):
            relation_list.append(field.name)
            next_model = field.related_model
        elif isinstance(field, ManyToManyRel):
            relation_list.append(field.get_accessor_name())
            next_model = field.through
        elif isinstance(field, ForeignObjectRel):
            relation_list.append(field.get_accessor_name())
            next_model = field.related_model
        else:
            continue

        add_model_to_process(next_model, to_process, result_dict)

    relation_list.sort()


def model_label(model):
    return '{}.{}'.format(model._meta.app_label, model._meta.object_name)


def add_model_to_process(model, to_process, result_dict):
    if model not in to_process and model_label(model) not in result_dict:
        to_process.append(model)


def override_fields(instance, _override_fields: OverrideFieldDict):
    """Overrides fields on instance."""
    for field_name, value in _override_fields.items():
        if not isinstance(value, OverrideFieldDict):
            value = value(instance) if isinstance(value, CallableValue) else value
            setattr(instance, field_name, value)
            continue
        nested_instance = getattr(instance, field_name)
        override_fields(nested_instance, value)
