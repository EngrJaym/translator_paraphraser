from django.urls import path
from . import views

urlpatterns = [
    path('', views.showParaphraser),
    path('paraphrase/', views.paraphrase_api, name='paraphrase_api'),
    path('translator', views.translate_api, name='translate_api')
]