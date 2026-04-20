
# import re
# from django.db.models import query
# from django.shortcuts import render
# from rest_framework import generics, serializers, status
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.response import Response
# from apps.carts.serializers import CartSerializer, CartUpdateSerializer, CartListSerializer
# from apps.products.models import Product
# from .models import Cart
# from apps.users.mixins import CustomLoginRequiredMixin
# from apps.users.models import User

# from config.helpers.error_response import error_response

# class CartList(CustomLoginRequiredMixin, generics.ListAPIView):
#     serializer_class = CartListSerializer
#     pagination_class = None

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.login_user.id)

# class CartAdd(CustomLoginRequiredMixin, generics.CreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

#     def post(self, request, *args, **kwargs):
        
#         self.get_serializer_class().validate(self, request.data)

#         product = Product.objects.filter(id=request.data['product']).first()
#         if (product is None):
#             return error_response('product not found.', status.HTTP_400_BAD_REQUEST)

#         cart = Cart.objects.filter(product_id=request.data['product'], user_id=request.login_user.id).first()
#         if (cart is not None):
#             return error_response('Cart already existed.', status.HTTP_400_BAD_REQUEST)

#         new_cart = Cart.objects.create(
#             user = User.objects.get(id=request.login_user.id),
#             product = product,
#             quantity = int( request.data['quantity'] )
#         )

#         # Convert Model to Serializer
#         serializer = CartListSerializer(new_cart)

#         # Response data as Dict
#         return Response(serializer.data)

# class CartUpdate(CustomLoginRequiredMixin, generics.UpdateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartUpdateSerializer
#     lookup_field = 'id'

#     def put(self, request, *args, **kwargs):
#         self.get_serializer_class().validate(self, request.data)
#         quantity = int(request.data['quantity'])

#         id = self.kwargs['id']
#         cart = Cart.objects.filter(id=id)
#         if cart.first() is None:
#             return error_response('Cart not found.', status.HTTP_400_BAD_REQUEST)

#         if quantity < 1:
#             cart.delete()
#             return Response({'message': 'Deleted successfully.'})

#         cart.update(
#             quantity = quantity
#         )

#         # Convert Model to Serializer
#         serializer = CartListSerializer(cart[0])

#         # Response data as Dict
#         return Response(serializer.data)

from rest_framework import generics, status
from rest_framework.response import Response

from apps.carts.serializers import (
    CartSerializer,
    CartUpdateSerializer,
    CartListSerializer
)
from apps.products.models import Product
from .models import Cart
from apps.users.mixins import CustomLoginRequiredMixin
from apps.users.models import User
from config.helpers.error_response import error_response


class CartList(CustomLoginRequiredMixin, generics.ListAPIView):
    serializer_class = CartListSerializer
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.login_user.id)


class CartAdd(CustomLoginRequiredMixin, generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.filter(id=request.data.get("product")).first()
        if product is None:
            return error_response("Product not found.", status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(
            product_id=request.data.get("product"),
            user_id=request.login_user.id
        ).first()

        if cart is not None:
            return error_response("Cart already existed.", status.HTTP_400_BAD_REQUEST)

        new_cart = Cart.objects.create(
            user=User.objects.get(id=request.login_user.id),
            product=product,
            quantity=int(request.data.get("quantity"))
        )

        response_serializer = CartListSerializer(new_cart)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CartUpdate(CustomLoginRequiredMixin, generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartUpdateSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = int(request.data.get("quantity"))
        cart_id = self.kwargs["id"]

        cart = Cart.objects.filter(
            id=cart_id,
            user_id=request.login_user.id
        ).first()

        if cart is None:
            return error_response("Cart not found.", status.HTTP_400_BAD_REQUEST)

        if quantity < 1:
            cart.delete()
            return Response({"message": "Deleted successfully."}, status=status.HTTP_200_OK)

        cart.quantity = quantity
        cart.save()

        response_serializer = CartListSerializer(cart)
        return Response(response_serializer.data, status=status.HTTP_200_OK)