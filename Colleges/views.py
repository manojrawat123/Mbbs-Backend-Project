from rest_framework import viewsets, permissions
from .models import CollegeInfo
from .serializers import CollegeInfoSerializer
from django.db.models import Q

class CollegeInfoViewSet(viewsets.ModelViewSet):
    queryset = CollegeInfo.objects.all()
    serializer_class = CollegeInfoSerializer
    permission_classes = [permissions.IsAdminUser | permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        college_fee_total = self.request.query_params.get('fee')
        college_country = self.request.query_params.getlist('country')
        college_course_duration = self.request.query_params.get('course_duration')
        
        if college_fee_total:
            queryset = queryset.filter(college_fee_total__lte=college_fee_total)

        if college_country:
            country_filters = Q()
            for country in college_country:
                country_filters |= Q(college__college_country__iexact=country)

            queryset = queryset.filter(country_filters)

        if college_course_duration:
            queryset = queryset.filter(college_course_duration__lte=college_course_duration)

        return queryset