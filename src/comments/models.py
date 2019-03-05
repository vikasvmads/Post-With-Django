from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from posts.models import Post


class commentsManager(models.Manager):
        def all(self):
                qs = super(commentsManager , self).filter(parent=None)
                return qs

        def filter_by_instance(self , instance):
                content_type = ContentType.objects.get_for_model(instance.__class__)
                qs =  super(commentsManager , self).filter(
                        content_type=content_type , object_id=instance.id
                        ).filter(parent=None)
                return qs


class comments(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, default=1 ,on_delete=None)
    #comments = models.ForeignKey(Post ,on_delete=None)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent     = models.ForeignKey("self" , null=True , blank=True ,on_delete=models.CASCADE)

    content  = models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True)

    objects = commentsManager()

    class Meta:
            ordering = ['-timestamp']

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    def children(self):
        return comments.objects.filter(parent=self)

    def get_absolute_url(self):
        return reverse("comments:comment_thread", kwargs={"id": self.id})

    @property
    def is_parent(self):
            if self.parent is None:
                    return False
            return True
