from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password 
from django.db import IntegrityError 
from django.shortcuts import redirect 
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from business_info.models import (
    Policy,
    FAQCategory,
    SiteConfig
)
from document_manager.models import (
    Document,
    Category
)
from store.models import (
    DocumentBundle
)


class HomePageView(TemplateView):

    template_name = "webclient/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bundles'] = DocumentBundle.objects.alive()
        context['categories'] = Category.objects.filter(deleted_at=None)
        return context


class PoliciesView(TemplateView):

    template_name = "webclient/policies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['policies'] = Policy.objects.all()
        return context


class FAQView(TemplateView):

    template_name = "webclient/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq_categories'] = FAQCategory.objects.all()
        return context


class AboutUsView(TemplateView):

    template_name = "webclient/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_config = SiteConfig.objects.last()
        if site_config:
            context['title'] = site_config.about_page_title
            context['content'] = site_config.about_page_content
            context['image'] = site_config.about_page_image
        return context


class DocumentDetailView(DetailView):

    model = Document


class SignupView(TemplateView):

    template_name = "webclient/register.html"

    def post(self, request, *args, **kwargs):
        redirect_url = 'signup'
        try:
            email = request.POST['email']
            password = request.POST['password']
            password = make_password(password)
            user = User(
                username = email,
                password = password
            )
            user.save()
        except KeyError:
            msg = 'Some required fields are empty'
            tag = messages.WARNING
        except IntegrityError:
            msg = 'The user already exists'
            tag = messages.WARNING
        except Exception as e:
            msg = 'Error: ' + str(e)
            tag = messages.WARNING
        else:
            msg = '¡Success!'
            tag = messages.SUCCESS
            redirect_url = 'login'

        messages.add_message(request, tag, msg)
        
        return redirect(redirect_url)



