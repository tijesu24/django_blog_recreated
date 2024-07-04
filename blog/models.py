from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from filer.fields.image import FilerImageField

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

from django.utils import timezone
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    cover_image = FilerImageField(null=True, blank=True,
                                  related_name="cover_image", on_delete=models.CASCADE)
    content = CKEditor5Field(
        'Text', config_name='extends', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    date_published = models.DateTimeField(null=True, blank=True)  # New field
    more_pic = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ['-created_on']
        permissions = [

            ("publish_post", "Can publish post"),

        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", kwargs={"slug": str(self.slug)})
    

    def save(self, *args, **kwargs):
        # Update the publish date
        if self.status == 1 and self.date_published is None: 
            self.date_published = timezone.now()
        elif self.status == 0:
            self.date_published = None
            
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']
        permissions = [

            ("edit_comment_content", "Can edit comment"),


        ]

    def __str__(self) -> str:
        # Use strftime to format the datetime object
        formatted_date = self.created_on.strftime('%B %d, %Y at %I:%M %p')
        return f'Comment by {self.name} on {formatted_date}'
