from django.urls import path
from . import views
from .views  import ProductDetailView

urlpatterns=[
    path('', views.home, name='home'),
    # path('view/<int:pk>/', views.view, name='view'),
    path('view/<int:pk>/',ProductDetailView.as_view() ,name='view'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),
    path('payment/', views.payment, name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('paypal/', views.paypal, name='paypal'),
    path('daraja/stk-push', views.stk_push_callback, name='stk_push_callback'),

]