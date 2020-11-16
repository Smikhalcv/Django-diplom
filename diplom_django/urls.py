"""diplom_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shop.views import main, cart, smartphones, empty_section, phone, feedback, add_to_cart, registration, order

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', main, name='main'),
    path(r'registration/', registration, name='registration'),
    path(r'login/', LoginView.as_view(template_name='login.html'), name='login'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
    path(r'cart/', cart, name='cart'),
    path(r'smartphones/', smartphones, name='smartphones'),
    path(r'empty_section/', empty_section, name='empty_section'),
    path(r'phone/<slug:slug>/', phone, name='phone'),
    path(r'feedback/<slug:slug>/', feedback, name='feedback'),
    path(r'add_to_cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path(r'order/<id>/', order, name='order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
       path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
