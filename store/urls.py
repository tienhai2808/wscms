from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='home'),
  path('dang-ky/', views.sign_up, name='sign-up'),
  path('dang-nhap/', views.sign_in, name='sign-in'),
  path('dang-xuat/', views.logout, name='logout'),
  path('dat-hang/', views.order, name='order'),
  path('don-hang/', views.my_order, name='my-order'),
  path('don-hang/<int:export_id>/', views.order_detail, name='order-detail'),
  path('ho-so/', views.profile, name='profile'),
  path('sua-ho-so/<str:username>/', views.update_profile, name='update-profile'),
  path('san-pham/<slug:cat_slug>/', views.category, name='category'),
  path('<slug:cat_slug>/<slug:pro_slug>/', views.product, name='product')
]