from rest_framework import serializers

from Task.Program.models import ModelQ, ModelQQ


class SerializerM(serializers.Serializer):
    id = serializers.IntegerField(required=False,allow_null=True)
    id_modelQ = serializers.PrimaryKeyRelatedField(required=False,queryset=ModelQ.objects.all())
    name_address = serializers.CharField(max_length=100)
    latitude_coordinate_x = serializers.FloatField()
    longtitude_coordinate_y = serializers.FloatField()
    distance_to_MKAD= serializers.CharField()
    class Meta:
        model = ModelQQ
        exclude = []
    def create(self, validated_data):
        resp = ModelQQ.objects.create(**validated_data)
        return resp

class SerializerQ(serializers.Serializer):

    id = serializers.IntegerField(required=False,allow_null=True)
    array_address = SerializerM(write_only=True,many=True,allow_null=True)
    req_modelQQs= SerializerM(read_only=True,source="modelqq_set",many=True,allow_null=True)
    # names = serializers.CharField(read_only=True,source="modelqq_set")
    request_address = serializers.CharField(max_length=100)
    date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = ModelQ
        exclude = []
    def create(self, validated_data):
        reqes = validated_data.pop("array_address")
        resp = ModelQ.objects.create(**validated_data)
        for e in reqes:
            e["id_modelQ"] = resp.id
        # reqes["id_modelQ"] = resp.id
        test = SerializerM(data=reqes,many=True)
        if test.is_valid(raise_exception=True):
            test.save()
        return resp


