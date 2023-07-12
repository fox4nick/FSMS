from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, NewRequestModel
from itertools import chain
from operator import attrgetter

class Index(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'employee/index.html')
		
class About(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'employee/about.html')

class Dashboard(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		# Populate dashboard with today's and all waiting requests.
		if request.user.is_superuser:
			today = datetime.today()
			orders = OrderModel.objects.filter(
				Q(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day) |
				Q(status="Deferred") |
				Q(status="Pending")
				).order_by()
			new_requests = NewRequestModel.objects.filter(
				Q(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day) |
				Q(status="Deferred") |
				Q(status="Pending")
				).order_by()
		# Populate dashboard with all entries pertaining to logged in user.
		else:
			orders = OrderModel.objects.filter(
				email=request.user.email)
			new_requests = NewRequestModel.objects.filter(
				email=request.user.email)

		# loop through the orders check if order is fulfilled
		pending_orders = []
		for order in orders:
			if order.status == "Pending":
				pending_orders.append(order)

		pending_requests = []
		for new_request in new_requests:
			if new_request.status == "Pending":
				pending_requests.append(new_request)

		# pass total number of orders into template
		context = {
			'orders': orders,
			'pending_orders': len(pending_orders),
			'total_orders': len(orders),
			'new_requests': new_requests,
			'pending_requests': len(pending_requests),
			'total_requests': len(new_requests)
		}

		return render(request, 'employee/dashboard.html', context)

	def test_func(self):
		return self.request.user.groups.filter(name='Staff').exists()

class Menu(View):
	def get(self, request, *args, **kwargs):
		snacks = MenuItem.objects.filter(category__name__contains='Snack').order_by('name')
		drinks = MenuItem.objects.filter(category__name__contains='Drink').order_by('name')
		menu_items = list(chain(snacks, drinks))

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
		).order_by('name')

		context = {
			'menu_items': menu_items
		}

		return render(request, 'employee/menu.html', context)

class NewRequest(View):
	def get(self, request, *args, **kwargs):
		# pass into context
		context = {
			
		}

		#render the template
		return render(request, 'employee/new_request.html', context)

	def post(self, request, *args, **kwargs):
		snack = request.POST.get('snack')
		argument = request.POST.get('argument')
		link = request.POST.get('link')
		name = request.POST.get('name')
		email = request.POST.get('email')

		new_request = NewRequestModel.objects.create(
			snack=snack,
			argument=argument,
			link=link,
			name=name,
			email=email
		)

		# After everything is done, send confirmation email to the user
		body = ('Dear ' + name + ',\n\n'
			'We have received your request, and it is now awaiting approval. We will let you know as soon as we have any updates!\n\n'
			'Request Summary:' +
			'\nSnack: ' + snack +
			'\nArgument: ' + argument +
			'\nLink: ' + link +
			'\n\nThank you for your request!\n\n'
			'Sincerely,\n'
			'The Fox Sustenance Management Team')

		send_mail(
			'Thank You For Your Request!',
			body,
			'example@email.com',
			[email],
			fail_silently=False
		)

		context = {
			'snack': snack,
			'argument': argument,
			'link': link,
		}

		return render(request, 'employee/new_request_confirmation.html', context)

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
		item_ids = []

		for item in items:
			menu_item = MenuItem.objects.get(pk=int(item))
			item_data = {
				'id': menu_item.pk,
				'name': menu_item.name,
			}

			order_items['items'].append(item_data)

		for item in order_items['items']:
			item_ids.append(item['id'])

		order = OrderModel.objects.create(
			name=name,
			email=email
		)
		order.items.add(*item_ids)

		request_summary = ''

		for item in order.items.all().order_by('name'):
			request_summary = request_summary + item.name + '\n'

		# After everything is done, send confirmation email to the user
		body = ('Dear ' + name + ',\n\n'
			'We have received your request, and it is now awaiting approval. We will let you know as soon as we have any updates!\n\n'
			'Request Summary:\n' +
			request_summary +
			'\nThank you for your request!\n\n'
			'Sincerely,\n'
			'The Fox Sustenance Management Team')

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

class NewRequestDetails(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		new_request = NewRequestModel.objects.get(pk=pk)

		context = {
			'new_request': new_request,
		}

		return render(request, 'employee/new-request-details.html', context)

	def post(self, request, pk, *args, **kwargs):
		new_request = NewRequestModel.objects.get(pk=pk)
		new_request.status = request.POST.get('radio_status')
		new_request.save()

		# Send email update to user who placed request.
		if new_request.status == "Fulfilled":
			body = ('Dear ' + new_request.name + ',\n\n'
				'Congratulations! Your request has been fulfilled! You can expect to see your snack/drink available very soon!\n\n'
				'Request Summary:' +
				'\nSnack: ' + new_request.snack +
				'\nArgument: ' + new_request.argument +
				'\nLink: ' + new_request.link +
				'\n\nThank you for your request!\n\n'
				'Sincerely,\n'
				'The Fox Sustenance Management Team')
		elif new_request.status == "Deferred":
			body = ('Dear ' + new_request.name + ',\n\n'
				'Your request has been deferred. An administrator will revisit your request as soon as possible. Thank you for your patience!\n\n'
				'Request Summary:' +
				'\nSnack: ' + new_request.snack +
				'\nArgument: ' + new_request.argument +
				'\nLink: ' + new_request.link +
				'\n\nThank you for your request!\n\n'
				'Sincerely,\n'
				'The Fox Sustenance Management Team')
		elif new_request.status == "Denied":
			body = ('Dear ' + new_request.name + ',\n\n'
				'We regret to inform you that your request has been denied. We are not able to procure provide your snack/drink at this time.\n\n'
				'Request Summary:' +
				'\nSnack: ' + new_request.snack +
				'\nArgument: ' + new_request.argument +
				'\nLink: ' + new_request.link +
				'\n\nThank you for your request!\n\n'
				'Sincerely,\n'
				'The Fox Sustenance Management Team')

		send_mail(
			'Your Request Has Been Updated!',
			body,
			'example@email.com',
			[new_request.email],
			fail_silently=False
		)

		context = {
			'new_request': new_request,
		}

		return render(request, 'employee/new-request-details.html', context)

	def test_func(self):
		return self.request.user.groups.filter(name='Staff').exists()

class OrderDetails(LoginRequiredMixin, View):
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

		return render(request, 'employee/order-details.html', context)

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

		return render(request, 'employee/order-details.html', context)

	def test_func(self):
		return self.request.user.groups.filter(name='Staff').exists()