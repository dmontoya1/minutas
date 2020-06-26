from rest_framework import serializers
from .models import Policy, FAQItem, FAQCategory


class PolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = ('policy_type', 'content')


class FAQItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQItem
        fields = ('id', 'question', 'answer')


class FAQCategorySerializer(serializers.ModelSerializer):
    faqitem_set = FAQItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = FAQCategory
        fields = ('id', 'name', 'faqitem_set')
