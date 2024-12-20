from django.urls import path
from . import views

urlpatterns = [
  path('', views.index,name='manage'),
  path('bao-cao/', views.report, name='report'),
  path('nguoi-dung/', views.users , name='users'),
  path('them-nhan-vien/', views.create_emp, name='create-employee'),
  path('nguoi-dung/<int:user_id>/', views.user_detail, name='user-detail'),
  path('nhap-hang/', views.import_product, name='import'),
  path('nhap-hang/<int:import_id>/', views.import_detail, name='import-detail'),
  path('san-pham/', views.products, name='manage-product'),
  path('san-pham/<int:pro_id>/', views.product_detail, name='manage-product-detail'),
  path('san-pham/chinh-sua/<int:pro_id>/', views.product_cu, name='manage-product-update'),
  path('san-pham/tao-moi/', views.product_cu, name='manage-product-create'),
  path('nha-cung-cap/', views.providers, name='providers'),
  path('nha-cung-cap/tao-moi/', views.create_provider, name='create-provider' )
]