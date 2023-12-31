from django.http import HttpResponse
import logging
from .models import Order, Product, Client
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, datetime

logger = logging.getLogger(__name__)


def main(request):
    html = """
    <h1>Добро пожаловать на мой первый Django сайт!</h1>
    <p>Здесь вы найдете много интересного!</p>
    """
    logger.info('Посещена главная страница')
    return HttpResponse(html)


def about(request):
    html = """
    <h1>Обо мне</h1>
    <p>Привет! Я - разработчик Django.</p>
    """
    logger.info('Посещена страница "О себе"')
    return HttpResponse(html)


def create_client(name, email, phone_number, address):
    client = Client(name=name, email=email, phone_number=phone_number, address=address)
    client.save()
    return client


# Получение всех клиентов
def get_all_clients(request):
    clients = Client.objects.all()
    return HttpResponse(clients)


# Получение клиента по его ID
def get_client_by_id(client_id):
    return Client.objects.get(pk=client_id)


# Обновление информации о клиенте
def update_client(client, name, email, phone_number, address):
    client.name = name
    client.email = email
    client.phone_number = phone_number
    client.address = address
    client.save()


# Удаление клиента
def delete_client(client):
    client.delete()


# Создание нового товара
def create_product(name, description, price, quantity):
    product = Product(name=name, description=description, price=price, quantity=quantity)
    product.save()
    return product


# Получение всех товаров
def get_all_products(request):
    products = Product.objects.all()
    return HttpResponse(products)


# Получение товара по его ID
def get_product_by_id(product_id):
    return Product.objects.get(pk=product_id)


# Обновление информации о товаре
def update_product(product, name, description, price, quantity):
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    product.save()


# Удаление товара
def delete_product(product):
    product.delete()


# Создание нового заказа
def create_order(client, products, total_amount):
    order = Order(client=client, total_amount=total_amount)
    order.save()
    order.products.set(products)
    return order


# Получение всех заказов
def get_all_orders(request):
    orders = Order.objects.all()
    return HttpResponse(orders)


# Получение заказа по его ID
def get_order_by_id(order_id):
    return Order.objects.get(pk=order_id)


# Обновление информации о заказе
def update_order(order, client, products, total_amount):
    order.client = client
    order.total_amount = total_amount
    order.save()
    order.products.set(products)


# Удаление заказа
def delete_order(order):
    order.delete()


# def order_list(request):
#     client = request.user  # Предполагается, что клиент авторизован
#     current_date = timezone.now()
#
#     # Заказы за последние 7 дней (неделю)
#     products_week = client.orders.filter(order_date__gte=current_date - timezone.timedelta(days=7)).values(
#         'products__name').distinct()
#
#     # Заказы за последние 30 дней (месяц)
#     products_month = client.orders.filter(order_date__gte=current_date - timezone.timedelta(days=30)).values(
#         'products__name').distinct()
#
#     # Заказы за последние 365 дней (год)
#     products_year = client.orders.filter(order_date__gte=current_date - timezone.timedelta(days=365)).values(
#         'products__name').distinct()
#
#     context = {
#         'products_week': products_week,
#         'products_month': products_month,
#         'products_year': products_year
#     }
#
#     return render(request, 'template.html', context)

def list_goods_period_of_time(request, days, pk):
    """Выводит список добавленных клиентом товаров из всех его заказов"""
    today = datetime.now()
    range_days = today - timedelta(days=days)
    client = Client.objects.filter(pk=pk).first()
    orders = Order.objects.filter(client=client, order_date__range=(range_days, today)).all()
    context = {
        'days': days,
        'range_days': range_days,
        'name': client.name,
        'orders': orders,
        'count': len(orders),
    }
    return render(request, './hw_3/list_goods_period_of_time.html', context)


def show_client_orders(request, pk):
    """Вывод всех заказов клиента"""
    client = Client.objects.filter(pk=pk).first()
    orders = Order.objects.filter(client=client).all()

    context = {
        'name': client.name,
        'count': len(orders),
        'orders': orders,
    }
    return render(request, './hw_3/show_client_orders.html', context)
