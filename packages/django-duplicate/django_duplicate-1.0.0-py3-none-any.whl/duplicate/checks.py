from django.conf import settings
from django.core.checks import (
    Error,
    register,
)

from .utils import (
    generate_known_relations_dict,
    load_model_from_str,
)


@register()
def duplicate_models_check(app_configs, **kwargs):
    if not hasattr(settings, 'DJANGO_DUPLICATE_KNOWN_RELATIONS'):
        return [Error(
            'You don\'t have DJANGO_DUPLICATE_KNOWN_RELATIONS declared in settings!',
            obj=settings,
            id='duplicate.E001',
        )]

    errors = []
    relations_dict = generate_known_relations_dict()

    hint = (
        'Probably some new relations or models was added to your project. '
        'Please analyze changes and their impact on your DuplicateMixin derivatives and then after adjusting your duplication calls '
        'add lacking entries to DJANGO_DUPLICATE_KNOWN_RELATIONS setting.'
    )

    for model, relations in relations_dict.items():
        if model not in settings.DJANGO_DUPLICATE_KNOWN_RELATIONS:
            errors.append(
                Error(
                    '[DuplicateMixin] Model that can be related by duplicate is not present in DJANGO_DUPLICATE_KNOWN_RELATIONS',
                    obj=load_model_from_str(model),
                    hint=hint,
                    id='duplicate.E002',
                )
            )
            continue

        current_relations = set(relations)
        saved_relations = set(settings.DJANGO_DUPLICATE_KNOWN_RELATIONS[model])

        if current_relations != saved_relations:
            not_present = current_relations - saved_relations
            removed = saved_relations - current_relations
            errors.append(
                Error(
                    (
                        '[DuplicateMixin] Not all model relations are properly saved in DJANGO_DUPLICATE_KNOWN_RELATIONS. '
                        'Not present relations: {not_present}; Relations removed from model: {removed}.'
                    ).format(
                        not_present=list(not_present),
                        removed=list(removed),
                    ),
                    hint=hint,
                    obj=load_model_from_str(model),
                    id='duplicate.E003',
                )
            )
            continue

    return errors
