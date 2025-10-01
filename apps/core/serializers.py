from rest_framework import serializers


class DynamicModelSerializer(serializers.ModelSerializer):
    """
    A dynamic ModelSerializer that can adapt to any model.
    """

    class Meta:
        model = None
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initialize serializer with dynamic model.

        The model must be passed as a kwarg 'model' when instantiating the serializer.
        """
        self.Meta.model = kwargs.pop("model", None)
        if not self.Meta.model:
            raise ValueError("You must pass a model to DynamicModelSerializer")
        super().__init__(*args, **kwargs)
