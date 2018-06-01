import re
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField


class Document(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True)
    content = RichTextField()

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = '{}'.format(slug)
        return unique_slug

    def __str__(self):
        self.get_fields()
        return self.name    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('document', kwargs={'slug': self.slug})

    def get_fields(self):
        c = str(self.content)        
        fields = []
        raw_fields = re.findall(r'{{(.*?)}}', c)
        for f in raw_fields:
            try:
                name, type = f.split('*')
            except ValueError:
                name = f
                type = False
            field = {}
            field['raw_name'] = name
            field['name'] = name.capitalize().replace('_', ' ')
            field['type'] = type 
            fields.append(field) 
        print(fields)
        return fields