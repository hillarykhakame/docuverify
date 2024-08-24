from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('upload', views.upload, name='upload'),
    path('verify', views.verify, name='verify'),
    path('text_extraction/<str:document_name>/', views.text_extraction, name='text_extraction'),
    path('verify_document/', views.verify_document_view, name='verify_document')

]
