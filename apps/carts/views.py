from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from apps.carts.serializers import CartSerializer, CartUpdateSerializer, CartListSerializer
from apps.products.models import Product
from .models import Cart
from apps.users.mixins import CustomLoginRequiredMixin
from apps.users.models import User


class CartList(CustomLoginRequiredMixin, generics.ListAPIView):
    serializer_class = CartListSerializer
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.login_user.id)


class CartAdd(CustomLoginRequiredMixin, generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        # Proper serializer validation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.filter(id=request.data.get('product')).first()
        if not product:
            raise NotFound("Product not found")

        existing_cart = Cart.objects.filter(
            product_id=product.id,
            user_id=request.login_user.id
        ).first()

        if existing_cart:
            raise ValidationError("Cart already exists")

        new_cart = Cart.objects.create(
            user=User.objects.get(id=request.login_user.id),
            product=product,
            quantity=int(request.data.get('quantity'))
        )

        return Response(CartListSerializer(new_cart).data, status=status.HTTP_201_CREATED)


class CartUpdate(CustomLoginRequiredMixin, generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartUpdateSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = int(request.data.get('quantity'))
        cart_id = self.kwargs.get('id')

        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            raise NotFound("Cart not found")

        if quantity < 1:
            cart.delete()
            return Response({"message": "Deleted successfully."}, status=status.HTTP_200_OK)

        cart.quantity = quantity
        cart.save()

        return Response(CartListSerializer(cart).data, status=status.HTTP_200_OK)