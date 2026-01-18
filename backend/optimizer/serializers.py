from rest_framework import serializers

class OptimizeRequestSerializer(serializers.Serializer):
    bullet = serializers.CharField(max_length=500)
    job_description = serializers.CharField(max_length=6000)

class OptimizeResponseSerializer(serializers.Serializer):
    optimized_bullet = serializers.CharField()
    similarity = serializers.FloatField()
    matched_keywords = serializers.ListField(child=serializers.CharField())
    missing_keywords = serializers.ListField(child=serializers.CharField())
