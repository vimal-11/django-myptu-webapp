from django.urls import path
from django.views.generic import TemplateView

app_name = 'feeds'

urlpatterns = [
    path('',TemplateView.as_view(template_name="feeds/index.html")),
    
    ]
