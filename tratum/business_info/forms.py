from django import forms
from django.core.files.images import get_image_dimensions
from .models import SliderItem, SiteConfig


class SliderItemForm(forms.ModelForm):

    class Meta:
        model = SliderItem
        fields = '__all__'

    def clean_image(self):
        picture = self.cleaned_data.get("image")
        if not picture:
            raise forms.ValidationError("La imagen es requerida")
        else:
            w, h = get_image_dimensions(picture)
            if w != 1920:
                raise forms.ValidationError("La imagen tiene un ancho de %i pixels, se requieren 1920 pixeles." % w)
            if h != 1080:
                raise forms.ValidationError("La imagen tiene un alto de %i pixels, se requieren 1080 pixeles" % h)
        return picture


class SiteConfigForm(forms.ModelForm):

    class Meta:
        model = SiteConfig
        fields = '__all__'

    def clean_about_page_image(self):
        picture = self.cleaned_data.get("about_page_image")
        if not picture:
            raise forms.ValidationError("La imagen es requerida")
        else:
            w, h = get_image_dimensions(picture)
            if w != 800:
                raise forms.ValidationError("La imagen tiene un ancho de %i pixels, se requieren 800 pixeles." % w)
            if h != 1000:
                raise forms.ValidationError("La imagen tiene un alto de %i pixels, se requieren 1000 pixeles" % h)
        return picture
