from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from employee.models import OrderModel

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
	def get(self, request, *args, **kwargs):
		# get the current date
		today = datetime.today()
		orders = OrderModel.objects.filter(
			created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
		#orders = OrderModel.objects.all()

		# loop through the orders check if order is fulfilled
		deferred_orders = []
		for order in orders:
			if order.status == "Deferred":
				deferred_orders.append(order)

		# pass total number of orders into template
		context = {
			'orders': orders,
			'deferred_orders': len(deferred_orders),
			'total_orders': len(orders)
		}

		return render(request, 'rule4/dashboard.html', context)

	def test_func(self):
		return self.request.user.groups.filter(name='Staff').exists()

class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
	def get(self, request, pk, *args, **kwargs):
		order = OrderModel.objects.get(pk=pk)
		
		order_items = {
			'items': []
		}

		order_items['items'] = order.items.all()

		context = {
			'order': order,
			'items': order_items['items'],
		}

		return render(request, 'rule4/order-details.html', context)

	def post(self, request, pk, *args, **kwargs):
		order = OrderModel.objects.get(pk=pk)
		order.status = request.POST.get('radio_status')
		order.save()

		order_items = {
			'items': []
		}

		order_items['items'] = order.items.all()

		context = {
			'order': order,
			'items': order_items['items'],
		}

		return render(request, 'rule4/order-details.html', context)

	def test_func(self):
		return self.request.user.groups.filter(name='Staff').exists()