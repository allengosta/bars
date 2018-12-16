from rest_framework import serializers

from new_app.models import Candidate, Teacher


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name', 'planet', 'age', 'email']


class TeacherSerializer(serializers.ModelSerializer):
    planet = serializers.SerializerMethodField()
    kolvo = serializers.IntegerField()

    def get_planet(self, obj):
        return obj.planet.name

    class Meta:
        model = Teacher
        fields = ['name', 'planet', 'kolvo']


class TeacherListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['name', 'id']