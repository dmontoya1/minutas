
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'webclient'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('policies/', views.PoliciesView.as_view(), name='policies'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('document/<slug:slug>/', views.DocumentDetailView.as_view(), name='document'),
    path('documents/', views.DocumentsView.as_view(), name='documents')
]