from rest_framework import serializers
from .models import College, CollegeMedia, CollegeInfo,University,FeeStructure

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'


class CollegeMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeMedia
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'



class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class CollegeInfoSerializer(serializers.ModelSerializer):
    college = CollegeSerializer()
    colege_fee_info= FeeStructureSerializer()
    college_extra_info= UniversitySerializer()
    college_media = CollegeMediaSerializer(many=True)

    class Meta:
        model = CollegeInfo
        fields = '__all__'
