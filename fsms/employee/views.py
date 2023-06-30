from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel

class Index(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'employee/index.html')
		
class About(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'employee/about.html')

class Order(View):
	def get(self, request, *args, **kwargs):
		# get every item from each category
		snacks = MenuItem.objects.filter(category__name__contains='Snack')
		drinks = MenuItem.objects.filter(category__name__contains='Drink')

		# pass into context
		context = {
			'snacks': snacks,
			'drinks': drinks,
		}

		#render the template
		return render(request, 'employee/order.html', context)

	def post(self, request, *args, **kwargs):
		order_items = {
			'items': []
		}

		items = request.POST.getlist('items[]')

		for item in items:
			menu_item = MenuItem.objects.get(pk=int(item))
			item_data = {
				'id': menu_item.pk,
				'name': menu_item.name,
				'price': menu_item.price
			}

			order_items['items'].append(item_data)

			price = 0
			item_ids = []

		for item in order_items['items']:
			price += item['price']
			item_ids.append(item['id'])

		order = OrderModel.objects.create(price=price)
		order.items.add(*item_ids)

		context = {
			'items': order_items['items'],
			'price': price
		}

		return render(request, 'employee/order_confirmation.html', context)