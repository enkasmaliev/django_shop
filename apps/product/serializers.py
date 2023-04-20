from rest_framework import serializers
from django.db import models
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        return [{
            'title': item.title,
            'slug': item.slug,
            'user': item.user.username,
            'price': item.price,
            'main_image': item.main_image.url
        } for item in iterable]


class ProductSerializer(serializers.ModelSerializer):
    imgs = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    user = serializers.ReadOnlyField(source='user.username')


    class Meta:
        model = Product
        fields = '__all__'
        # exclude = 'все_поля_кроме_поля_которое_нужно_пропустить'
        read_only_fields = ['slug']
        list_serializer_class = ProductListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['carousel'] = ProductImageSerializer(
            instance.images.all(), many=True).data
        return representation
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        imgs = validated_data.pop('imgs', None)
        product = Product.objects.create(**validated_data)
        if imgs is not None:
            images = []
            for image in imgs:
                images.append(ProductImage(product=product, image=image))
            ProductImage.objects.bulk_create(images)
        return product
