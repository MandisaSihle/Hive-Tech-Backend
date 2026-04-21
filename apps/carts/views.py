from rest_framework import generics, status
from rest_framework.response import Response

from apps.carts.models import Cart
from apps.carts.serializers import CartListSerializer, CartUpdateSerializer
from apps.products.models import Product
from apps.users.mixins import CustomLoginRequiredMixin
from apps.users.models import User
from config.helpers.error_response import error_response


# =========================
# CART LIST
# =========================
class CartList(CustomLoginRequiredMixin, generics.ListAPIView):
    serializer_class = CartListSerializer
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.login_user.id)


# =========================
# CART ADD / INCREMENT
# =========================
class CartAdd(CustomLoginRequiredMixin, generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer  # we return response manually

    def post(self, request, *args, **kwargs):
        try:
            user = getattr(request, "login_user", None)

            if not user:
                return error_response(
                    "User not authenticated",
                    status.HTTP_401_UNAUTHORIZED
                )

            product_id = request.data.get("product")
            quantity = request.data.get("quantity")

            if not product_id or not quantity:
                return error_response(
                    "Product and quantity are required",
                    status.HTTP_400_BAD_REQUEST
                )

            product = Product.objects.filter(id=product_id).first()

            if not product:
                return error_response(
                    "Product not found",
                    status.HTTP_400_BAD_REQUEST
                )

            # Check if cart already exists
            cart = Cart.objects.filter(
                user_id=user.id,
                product_id=product_id
            ).first()

            # If exists → update quantity
            if cart:
                cart.quantity += int(quantity)
                cart.save()

                return Response(
                    CartListSerializer(cart).data,
                    status=status.HTTP_200_OK
                )

            # Else → create new cart
            new_cart = Cart.objects.create(
                user_id=user.id,
                product=product,
                quantity=int(quantity)
            )

            return Response(
                CartListSerializer(new_cart).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print("CART ADD ERROR:", str(e))
            return error_response(
                "Internal server error",
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =========================
# CART UPDATE / DELETE
# =========================
class CartUpdate(CustomLoginRequiredMixin, generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartUpdateSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        try:
            user = getattr(request, "login_user", None)

            if not user:
                return error_response(
                    "User not authenticated",
                    status.HTTP_401_UNAUTHORIZED
                )

            quantity = request.data.get("quantity")
            cart_id = kwargs.get("id")

            if quantity is None:
                return error_response(
                    "Quantity is required",
                    status.HTTP_400_BAD_REQUEST
                )

            cart = Cart.objects.filter(
                id=cart_id,
                user_id=user.id
            ).first()

            if not cart:
                return error_response(
                    "Cart not found",
                    status.HTTP_404_NOT_FOUND
                )

            quantity = int(quantity)
            # If quantity is 0 → delete cart
            if quantity < 1:
                cart.delete()
                return Response(
                    {"message": "Deleted successfully"},
                    status=status.HTTP_200_OK
                )

            cart.quantity = quantity
            cart.save()

            return Response(
                CartListSerializer(cart).data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("CART UPDATE ERROR:", str(e))
            return error_response(
                "Internal server error",
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )