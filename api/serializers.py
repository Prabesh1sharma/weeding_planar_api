from rest_framework import serializers

class RecommendationRequestSerializer(serializers.Serializer):
    city = serializers.CharField()
    category_name = serializers.CharField()

class RecommendationSerializer(serializers.Serializer):
    Name = serializers.CharField()
    Location = serializers.CharField()
    City = serializers.CharField()
    CategoryName = serializers.CharField()
    Image = serializers.CharField()
    Phone = serializers.CharField()
    avg_ratings = serializers.FloatField()
