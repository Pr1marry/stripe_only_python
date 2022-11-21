import os
import stripe
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from .models import Item, Order
from .serializers import ItemSerializer, OrderSerializer

stripe.api_key = os.getenv('API_KEY')


class BuyItemViewSet(viewsets.ViewSet):
    http_method_names = ['get']
    stripe.api_key = os.getenv('API_KEY')

    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )

        return redirect(session.url)


class BuyOrderViewSet(viewsets.ViewSet):
    http_method_names = ['get']
    stripe.api_key = os.getenv('API_KEY')

    def retrieve(self, request, pk=None):
        try:
            queryset = Item.objects.all()
            order = Order.objects.filter(pk=pk).values('multiply_items')
            items = []
            for element in range(len(order)):
                item = get_object_or_404(queryset, pk=order[element]['multiply_items'])
                serializer = ItemSerializer(item)
                items.append(serializer.data)

            line_items = []
            for el in items:
                line_item = {
                    'price_data': {
                        'currency': el['currency'],
                        'product_data': {
                            'name': el['name'],
                        },
                        'unit_amount': el['price'],
                    },
                    'quantity': 1,
                }
                line_items.append(line_item)

            session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url='http://localhost:8000/success',
                cancel_url='http://localhost:8000/cancel',
            )
            return redirect(session.url)
        except:
            return Response("can't search objects")


