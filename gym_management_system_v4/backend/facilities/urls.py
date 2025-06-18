from django.urls import path
from . import views

urlpatterns = [
    # 场馆类型
    path('types/', views.FacilityTypeListView.as_view(), name='facility_type_list'),
    path('types/<int:type_id>/', views.FacilityTypeDetailView.as_view(), name='facility_type_detail'),
    
    # 场馆管理
    path('', views.FacilityListView.as_view(), name='facility_list'),
    path('<int:facility_id>/', views.FacilityDetailView.as_view(), name='facility_detail'),
    path('<int:facility_id>/available-slots/', views.facility_available_slots_view, name='facility_available_slots'),
]

