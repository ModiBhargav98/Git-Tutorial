from django.urls import path
from .views import index, profile_update, add_product, remove_product, signup, stAPI, userpage, logout, sellerpage

urlpatterns = [
    path('', index),
    path('profile_update/', profile_update, name='profile_update'),
    path('add_product/', add_product, name='add_product'),
    path('remove_product/', remove_product, name='remove_product'),
    path('signup/', signup, name='signup'),
    path('userpage/', userpage, name='userpage'),
    path('seller/', sellerpage, name='seller'),
    path('logout/', logout, name='logout'),
    path('stapi/', stAPI)
]