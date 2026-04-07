from django.db import models

def check_references_and_get_deletable_instances(model_instance, ids):
    from django.apps import apps
    references_details = []
    deletable_instances = model_instance.objects.none()
    instances_to_check = model_instance.objects.filter(id__in=ids)

    if not instances_to_check.exists():
        return deletable_instances, references_details

    all_models = apps.get_models()
    for instance in instances_to_check:
        is_referenced = False
        for related_model in all_models:
            for field in related_model._meta.get_fields():
                if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                    if field.related_model == model_instance:
                        filter_kwargs = {field.name: instance}
                        if hasattr(related_model, 'deleted_by'):
                            filter_kwargs['deleted_by__isnull'] = True

                        related_objects = related_model.objects.filter(**filter_kwargs)

                        if related_objects.exists():
                            is_referenced = True
                            related_object_strs = [str(obj) for obj in related_objects[:5]]
                            references_details.append({
                                'related_model': related_model.__name__,
                                'related_objects': list(set(related_object_strs))
                            })

        if not is_referenced:
            deletable_instances |= model_instance.objects.filter(id=instance.id)

    return deletable_instances, references_details