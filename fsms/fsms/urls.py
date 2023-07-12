"""
URL configuration for fsms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from employee.views import Index, About, Order, NewRequest, Menu, MenuSearch, Dashboard, OrderDetails, NewRequestDetails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('rule4/', include('rule4.urls')),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('order/', Order.as_view(), name='order'),
    path('new/request/', NewRequest.as_view(), name='new-request'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('new_requests/<int:pk>/', NewRequestDetails.as_view(), name='new-request-details')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
