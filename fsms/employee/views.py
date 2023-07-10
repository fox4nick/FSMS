from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
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
		snacks = MenuItem.objects.filter(category__name__contains='Snack').order_by('name')
		drinks = MenuItem.objects.filter(category__name__contains='Drink').order_by('name')

		# pass into context
		context = {
			'snacks': snacks,
			'drinks': drinks,
		}

		#render the template
		return render(request, 'employee/order.html', context)

	def post(self, request, *args, **kwargs):
		name = request.POST.get('name')
		email = request.POST.get('email')

		order_items = {
			'items': []
		}

		items = request.POST.getlist('items[]')

		for item in items:
			menu_item = MenuItem.objects.get(pk=int(item))
			item_data = {
				'id': menu_item.pk,
				'name': menu_item.name,
			}

			order_items['items'].append(item_data)

			item_ids = []

		for item in order_items['items']:
			item_ids.append(item['id'])

		order = OrderModel.objects.create(
			name=name,
			email=email
		)
		order.items.add(*item_ids)

		# After everything is done, send confirmation email to the user
		body = ('Thank you for your order! Your food will be delivered soon!\n'
			'Thank you again for your order!')

		send_mail(
			'Thank You For Your Order!',
			body,
			'example@email.com',
			[email],
			fail_silently=False
		)

		context = {
			'items': order_items['items'],
		}

		return render(request, 'employee/order_confirmation.html', context)

class Menu(View):
	def get(self, request, *args, **kwargs):
		menu_items = MenuItem.objects.all()

		context = {
			'menu_items': menu_items
		}

		return render(request, 'employee/menu.html', context)

class MenuSearch(View):
	def get(self, request, *args, **kwargs):
		query = self.request.GET.get("q")

		menu_items = MenuItem.objects.filter(
			Q(name__icontains=query) |
			Q(description__icontains=query) |
			Q(category__name__contains=query)
		)

		context = {
			'menu_items': menu_items
		}

		return render(request, 'employee/menu.html', context)