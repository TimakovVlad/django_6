from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class StockProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = StockProductSerializer(many=True, source='stockproduct_set')

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('stockproduct_set')
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('stockproduct_set')
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        for position_data in positions_data:
            StockProduct.objects.update_or_create(
                stock=instance,
                product=position_data['product'],
                defaults={'quantity': position_data['quantity'],
                          'price': position_data['price']}
            )
        return instance
