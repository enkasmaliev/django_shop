from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']
        read_only_fields = ['total_cost']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_cost', 'created_at', 'updated_at', 'user', 'status']

    def create(self, validated_data: dict):
        validated_data['user'] = self.context.get('request').user
        items = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        total_order_cost = 0
        products = []
        for item in items:
            product = OrderItem(
                order=order,
                product=item['product'],
                quantity=item['quantity']
            )
            products.append(product)
            total_order_cost += product.total_cost
        order.total_cost = total_order_cost
        OrderItem.objects.bulk_Create(products)
        return order


