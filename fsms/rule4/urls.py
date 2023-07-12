from django.urls import path
from .views import OrderDetails, NewRequestDetails


urlpatterns = [
	path('orders/<int:pk>/', OrderDetails.as_view(), name='admin-order-details'),
	path('new_requests/<int:pk>/', NewRequestDetails.as_view(), name='admin-new-request-details')
]