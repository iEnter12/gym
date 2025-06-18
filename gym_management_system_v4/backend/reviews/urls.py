from django.urls import path
from . import views

urlpatterns = [
    # 评价管理
    path('', views.ReviewListView.as_view(), name='review_list'),
    path('user/', views.UserReviewListView.as_view(), name='user_review_list'),
    path('create', views.create_review_view, name='create_review'),
    path('<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('<int:review_id>/reply', views.reply_review_view, name='reply_review'),
    path('<int:review_id>/delete', views.delete_review_view, name='delete_review'),
    
    # 场馆评价
    path('facility/<int:facility_id>/', views.facility_reviews_view, name='facility_reviews'),
]

