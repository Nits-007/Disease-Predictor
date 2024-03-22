from django.urls import path
from .views import *



app_name = 'core'
urlpatterns = [
    path('', index,name='index'),
    path('check/',check, name='check'),
    path('patient_details/',patient_details, name='patient_details'),
    path('disease/', disease, name='disease'),
    path('detail/', detail, name='detail'),
    path('report/', report, name='report'),
    path('record/', record, name='record'),
    path('record/download',download,name='download'),
    path('record/detail/<int:id>', record_detail, name='record_detail'),
    path('add/',add,name='add'),
]