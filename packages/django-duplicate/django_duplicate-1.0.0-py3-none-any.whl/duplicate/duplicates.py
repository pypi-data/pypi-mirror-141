from contextlib import contextmanager
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

from django.db.models import (
    Field,
    FileField,
    ManyToManyField,
    Model,
)
from django.db.models.fields.related import (
    ForeignKey,
    OneToOneField,
    RelatedField,
)
from django.db.models.fields.reverse_related import (
    ForeignObjectRel,
    ManyToManyRel,
    ManyToOneRel,
    OneToOneRel,
)

from duplicate.utils import (
    CallableValue,
    OverrideFieldDict,
    override_fields as override_fields_util,
)

from .exceptions import NotNullableCircularRelation


empty = object()


class NestedSave(Exception):
    """NestedSave occurred."""

    def __init__(self, caller: 'Duplicate'):
        self.caller = caller

    def is_caller(self, duplicate: 'Duplicate') -> bool:
        return self.caller is duplicate


class NestedM2MOverride(Exception):
    pass


class Memoize(dict):

    def _build_key(self, instance: Model) -> Optional[Tuple[type, Any]]:
        return type(instance), instance.pk if instance is not None else None

    def __getitem__(self, key: Model) -> 'Duplicate':
        return super().__getitem__(self._build_key(key))

    def __setitem__(self, key: Model, value: 'Duplicate'):
        super().__setitem__(self._build_key(key), value)

    def __contains__(self, key: Model):
        return super().__contains__(self._build_key(key))


class Duplicate:

    def __init__(
        self,
        instance: Model,
        paths_graph: Dict[str, Dict],
        memo: Optional[Memoize]=None,
        override_fields: Optional[dict]=None,
        reference: bool=False,
    ):
        self.instance = instance
        self.during_relation_processing = False
        self.paths = paths_graph
        self.override_fields = override_fields or OverrideFieldDict()
        self.reference = reference

        self._relations = []
        self._reverse_relations = []
        self.postponed = []

        self.model = type(self.instance)
        self.memo = memo if memo is not None else Memoize()
        self.memo[self.instance] = self
        self.new_instance = self.build_new_instance() if not self.reference else self.instance

    def __repr__(self) -> str:
        return '<{}: {}>'.format(type(self).__name__, repr(self.instance))

    def build_new_instance(self) -> Model:
        instance = self.model()
        for field in self.model._meta.get_fields():

            if self.process_custom_field(instance, field, self.override_fields):
                continue

            elif isinstance(field, RelatedField):
                self.process_related_field(instance, field)

            elif isinstance(field, ForeignObjectRel):
                self.process_reverse_relation(instance, field)

            else:
                if field is self.model._meta.pk or any(field is parent._meta.pk for parent in self.model._meta.parents):
                    # Don't copy pk of model and any models parents
                    continue

                override_value = self.get_override_value(field.name)
                field_value = override_value if override_value is not empty else field.value_from_object(self.instance)
                if isinstance(field, FileField):
                    if field_value:
                        field_value.save(field_value.name, field_value.file, save=False)
                setattr(instance, field.name, field_value)

        return instance

    def process_related_field(self, instance: Model, field: RelatedField):
        override_field = self.get_override_value(field.name)
        if not isinstance(override_field, OverrideFieldDict) and override_field is not empty:
            if isinstance(field, ManyToManyField):
                raise NestedM2MOverride('You cannot override m2m relation.')
            setattr(instance, field.name, override_field)
            return

        if isinstance(field, ForeignKey):
            value = getattr(self.instance, field.name)
            if value is not None:
                if self.include_path(field.name) or self.include_path('*'):
                    self.register_direct_fk(value, field)
                    return
                elif self.include_path('~'):
                    self.register_direct_fk(value, field, reference=True)
                    return

            setattr(instance, field.name, value)

        elif isinstance(field, ManyToManyField):
            if self.include_path(field.name) or self.include_path('*'):
                value = field.remote_field.through._default_manager.filter(
                    **{field.m2m_field_name(): self.instance}
                )
                self.register_direct_m2m(value, field)

    def process_reverse_relation(self, instance: Model, rel: ForeignObjectRel):
        field_name = rel.get_accessor_name()

        if isinstance(rel, OneToOneRel):
            value = rel.related_model.objects.filter(
                **{rel.field.name: self.instance}
            ).first()
            if value is not None and self.include_path(field_name):
                self.register_reverse_o2o(value, rel)

        elif isinstance(rel, ManyToOneRel):
            if self.include_path(field_name):
                value = rel.related_model.objects.filter(
                    **{rel.field.name: self.instance}
                )
                self.register_reverse_fk(value, rel)

        elif isinstance(rel, ManyToManyRel):
            if self.include_path(field_name) or self.include_path('*'):
                value = rel.through._default_manager.filter(
                    **{rel.field.m2m_reverse_field_name(): self.instance}
                )
                self.register_reverse_m2m(value, rel)

    def process_custom_field(self, instance: Model, field: Field, override_fields: dict) -> bool:
        """Override this method to process some custom fields. Return True if field is processed and shouldn't be handled further."""
        return False

    def get_override_value(self, field_name: str) -> Any:
        override_value = self.override_fields.get(field_name, empty)
        return override_value(self.instance) if isinstance(override_value, CallableValue) else override_value

    def expand_reference(self, reference: bool=False, paths_graph: Dict[str, Dict]=None) -> 'Duplicate':
        if not reference and self.reference:
            self.paths = paths_graph or {}
            self.reference = False
            self.new_instance = self.build_new_instance()
        return self

    def save(self, parent: Optional['Duplicate']=None) -> Model:
        if self.new_instance.pk is not None:
            return self.new_instance

        if self.during_relation_processing:
            raise NestedSave(self)

        with self.relation_processing_context():
            for name, field, duplicate in self._relations:
                try:
                    self.save_relation(name, duplicate)
                except NestedSave as nested_save:
                    if nested_save.is_caller(self):
                        if field.null:
                            self.postponed.append(
                                lambda: self.save_deferred_relation(name, duplicate)
                            )
                        else:
                            raise NotNullableCircularRelation(self, duplicate)
                    elif field.null:
                        # Chain can be broke here. Register this branch to be processed after saving dependent model.
                        nested_save.caller.postponed.append(
                            lambda: self.save_deferred_relation(name, duplicate)
                        )
                    else:
                        raise

        self.new_instance.save()

        for action in self.postponed:
            action()

        if parent:
            # If this instance is saved in context of other, defer post save relations to end of parent processing.
            parent._reverse_relations.extend(self._reverse_relations)
            self._reverse_relations = []

        for duplicate in self._reverse_relations:
            duplicate.save()

        return self.new_instance

    def include_path(self, path: str) -> bool:
        return path in self.paths

    def register_direct_m2m(self, instances: Iterable[Model], field: ManyToManyField):
        paths_graph = self.paths.get(field.name, {})
        paths_graph.setdefault(field.m2m_field_name(), {})
        self._reverse_relations.extend([
            self.get_duplicate(instance, paths_graph=paths_graph) for instance in instances
        ])

    def register_reverse_m2m(self, instances: Iterable[Model], rel: ManyToManyRel):
        paths_graph = self.paths.get(rel.get_accessor_name(), {})
        paths_graph.setdefault(rel.field.m2m_reverse_field_name(), {})
        override_fields = self.override_fields.get(rel.get_accessor_name(), OverrideFieldDict())
        self._reverse_relations.extend([
            self.get_duplicate(instance, paths_graph=paths_graph, override_fields=override_fields) for instance in instances
        ])

    def register_direct_fk(self, instance: Model, field: Union[OneToOneField, ForeignKey], reference: bool = False):
        self._relations.append(
            (
                field.name,
                field,
                self.get_duplicate(
                    instance,
                    paths_graph=self.paths.get(field.name, {}),
                    override_fields=self.override_fields.get(field.name, OverrideFieldDict()),
                    reference=reference,
                )
            )
        )

    def register_reverse_fk(self, instances: Iterable[Model], rel: ForeignObjectRel):
        paths_graph = self.paths.get(rel.get_accessor_name(), {})
        paths_graph.setdefault(rel.field.name, {})
        override_fields = self.override_fields.get(rel.get_accessor_name(), OverrideFieldDict())
        self._reverse_relations.extend([
            self.get_duplicate(instance, paths_graph=paths_graph, override_fields=override_fields) for instance in instances
        ])

    def register_reverse_o2o(self, instance: Model, rel: OneToOneRel):
        paths_graph = self.paths.get(rel.get_accessor_name(), {})
        paths_graph.setdefault(rel.field.name, {})
        override_fields = self.override_fields.get(rel.get_accessor_name(), OverrideFieldDict())
        self._reverse_relations.append(self.get_duplicate(instance, paths_graph=paths_graph, override_fields=override_fields))

    def get_duplicate(
            self,
            instance: Model,
            paths_graph: Dict[str, Dict],
            override_fields: OverrideFieldDict = None,
            reference: bool = False
    ) -> 'Duplicate':
        override_fields = override_fields or OverrideFieldDict()
        if instance in self.memo:
            memoized_duplicate = self.memo[instance].expand_reference(reference, paths_graph)
            if override_fields:
                override_fields_util(memoized_duplicate.instance, override_fields)
            return memoized_duplicate
        return self.__class__(
            instance,
            memo=self.memo,
            paths_graph=paths_graph,
            reference=reference,
            override_fields=override_fields
        )

    def save_relation(self, name: str, duplicate: 'Duplicate'):
        setattr(self.new_instance, name, duplicate.save(self))

    def save_deferred_relation(self, name: str, duplicate: 'Duplicate'):
        current_value = getattr(self.new_instance, name)
        self.save_relation(name, duplicate)
        if current_value != getattr(self.new_instance, name):
            self.new_instance.save()

    @contextmanager
    def relation_processing_context(self):
        try:
            self.during_relation_processing = True
            yield
        finally:
            self.during_relation_processing = False


def extract_nested_paths(current_path: str, path_list: List[str]) -> List[str]:
    extracted_paths = []
    current_path_prefix = '{}.'.format(current_path)
    for path in path_list:
        if path.startswith(current_path_prefix):
            extracted_paths.append(path.replace(current_path_prefix, ''))
    return extracted_paths
