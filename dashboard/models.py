from django.db import models

class Page(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Widget(models.Model):
    title = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='widgets')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Link(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    icon_url = models.URLField(blank=True, null=True)
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='links')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
