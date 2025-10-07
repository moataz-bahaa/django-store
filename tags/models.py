from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TaggedItemManager(models.Manager):
    def get_tags_for(self, object_type, object_id):
        # get_form_model is a custom model that exists in ContentType
        content_type = ContentType.objects.get_for_model(object_type)
        queryset = TaggedItem.objects.select_related("tag").filter(
            content_type=content_type, object_id=object_id
        )
        return queryset


class Tag(models.Model):
    label = models.CharField(max_length=255)


# generic relationship
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = TaggedItemManager()
