from django.urls import path

# import store views
from store import views
# app name
app_name = 'store'
# store urls patterns
urlpatterns = [
    path('', views.IndexProductListView.as_view(), name='index'),
    path('details/<slug:slug>/', views.ProductDetailsView.as_view(), name='product_detail'),
]
