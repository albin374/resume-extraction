from django.urls import path
from . import views

urlpatterns = [
    path('', views.apply_job, name='apply_job'),
    path('success/<int:pk>/', views.application_success, name='application_success'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/application/<int:pk>/', views.admin_application_detail, name='admin_application_detail'),
    path('admin/application/<int:pk>/status/', views.update_status, name='update_status'),
]
