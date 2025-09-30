from rest_framework import serializers

def get_dynamic_serializer(model_class):
    """
    Returns a dynamic serializer for the given model class.
    """
    class DynamicSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'
    
    return DynamicSerializer