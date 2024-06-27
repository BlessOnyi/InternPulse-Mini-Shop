from django.shortcuts import render

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError



class ProductAPI(APIView):
    """
    Single API to handle product operations
    """
    serializer_class = ProductSerializer


    @swagger_auto_schema(operation_description="Retrieve all products", responses={200: ProductSerializer(many=True)})
    def get(self, request, format=None):
        products = Product.objects.all()

        return Response(
            {"data": self.serializer_class(products, many=True).data}, 
            status=status.HTTP_200_OK
            )

    @swagger_auto_schema(operation_description="Create a new product", request_body=ProductSerializer, responses={201: ProductSerializer})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                'status': 201,
                'success': True,
                'message': 'Successfully created',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except serializer.ValidationError as e:
            response_data = {
                'status': 400,
                'success': False,
                'message': f'Validation Error: {e.detail}'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'status': 500,
                'success': False,
                'message': f'Error occurred while creating new product: {str(e)}'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# THIS IS FOR FETCHING INDIVIDUAL PRODUCT
class ProductDetailAPI(APIView):
    """
    API to handle single product operations
    """
    serializer_class = ProductSerializer

    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)





class ProductUpdateAPI(APIView):
    """
    API view to update a product
    """
    serializer_class = ProductSerializer

    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 

    




class OrderAPI(APIView):
    """
    API to handle order operations
    """
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                'status': 201,
                'success': True,
                'message': 'Order successfully created',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            response_data = {
                'status': 400,
                'success': False,
                'message': f'Validation Error: {e.detail}'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'status': 500,
                'success': False,
                'message': f'Error occurred while creating order: {str(e)}'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





class OrderListAPI(APIView):
    """
    API to list all orders
    """
    def get(self, request, format=None):
        orders = Order.objects.filter(canceled=False)  # Exclude canceled orders
        if not orders.exists():
            response_data = {
                'status': 404,
                'success': False,
                'message': 'No active orders found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(orders, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)




class CancelOrderAPI(APIView):
    """
    API to cancel an order
    """
    serializer_class = OrderSerializer

    def put(self, request, pk, format=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        order.canceled = True
        order.save()
        serializer = self.serializer_class(order)
        response_data = {
            'status': 200,
            'success': True,
            'message': 'Order successfully canceled',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


    


