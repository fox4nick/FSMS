from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.mail import send_mail
from employee.models import OrderModel, NewRequestModel

class NewRequestDetails(LoginRequiredMixin, UserPassesTestMixin, View):
	def get(self, request, pk, *args, **kwargs):
		new_request = NewRequestModel.objects.get(pk=pk)

		context = {
			'new_request': new_request,
		}

		return render(request, 'rule4/new-request-details.html', context)

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
		elif new_request.status == "Pending":
			body = ('Dear ' + new_request.name + ',\n\n'
				'Your request is pending. An administrator will revisit your request as soon as possible. Thank you for your patience!\n\n'
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

		return render(request, 'rule4/new-request-details.html', context)

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

		# Send email update to user who placed request.
		if order.status == "Fulfilled":
			body = ('Dear ' + order.name + ',\n\n'
				'Congratulations! Your order has been fulfilled! You can expect to see your snack/drink available very soon!\n\n'
				'Order Summary:' +
				'\nSnack: ' + order.snack +
				'\nArgument: ' + order.argument +
				'\nLink: ' + order.link +
				'\n\nThank you for your order!\n\n'
				'Sincerely,\n'
				'The Fox Sustenance Management Team')
		elif order.status == "Deferred":
			body = ('Dear ' + order.name + ',\n\n'
				'Your order has been deferred. An administrator will revisit your order as soon as possible. Thank you for your patience!\n\n'
				'Order Summary:' +
				'\nSnack: ' + order.snack +
				'\nArgument: ' + order.argument +
				'\nLink: ' + order.link +
				'\n\nThank you for your order!\n\n'
				'Sincerely,\n'
				'The Fox Sustenance Management Team')
		elif order.status == "Denied":
			body = ('Dear ' + order.name + ',\n\n'
				'We regret to inform you that your order has been denied. We are not able to procure provide your snack/drink at this time.\n\n'
				'Order Summary:' +
				'\nSnack: ' + order.snack +
				'\nArgument: ' + order.argument +
				'\nLink: ' + order.link +
				'\n\nThank you for your order!\n\n'
				'Sincerely,\n'
				'The Fox Sustenance Management Team')
		elif order.status == "Pending":
			body = ('Dear ' + order.name + ',\n\n'
				'Your order his pending. An administrator will revisit your order as soon as possible. Thank you for your patience!\n\n'
				'Order Summary:' +
				'\nSnack: ' + order.snack +
				'\nArgument: ' + order.argument +
				'\nLink: ' + order.link +
				'\n\nThank you for your order!\n\n'
				'Sincerely,\n'
				'The Fox Sustenance Management Team')

		send_mail(
			'Your Order Has Been Updated!',
			body,
			'example@email.com',
			[order.email],
			fail_silently=False
		)

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