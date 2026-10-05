from django.urls import path,include
from Products import views

# here to give path
urlpatterns = [
    path('product_listing/<slug:slug>/',views.product_listing ,name="product_listing"),
    path('brand/<slug:slug>/', views.brand_product_listing, name='brand_product_listing'),   
    path('product_listing/product_page/<slug:slug>',views.product_page,name="product_page"),
]


