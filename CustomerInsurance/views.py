from django.shortcuts import render

# 3rd party imports
from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from.serializers import PolicySerializer

from .models import Policy, Customer
from django.db.models.functions import TruncMonth
from django.db.models import Count

from .filters import PolicyFilter
# Create your views here.


class PolicyViewSet(viewsets.ModelViewSet):
    """
        list
        serializer : CustomerInsurance.serializers.PolicySerializer
    """
    serializer_class = PolicySerializer
    filter_class = PolicyFilter
    queryset = Policy.objects.all()
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        '''
        :param request:
        :param args:
        :param kwargs:
        :return:
            List all policies
        '''
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
            Update Policy data
            date of purchase is not editable
        """
        date = request.data.pop('date_of_purchase', None)
        if date:
            return Response({"message":"Should not allowed to change date of purchase"}, status=status.HTTP_400_BAD_REQUEST)
        return super(PolicyViewSet, self).update(request, *args, **kwargs)


class ProgressViewSet(viewsets.GenericViewSet):

    '''
        views to get number of policies bought in every month.
    '''

    queryset = Policy.objects.all()
    http_method_names = ['get']

    def list(self, request):

        try:
            lis1=[]
            import datetime
            data = Policy.objects.annotate(month=TruncMonth('date_of_purchase')).values('month').annotate(
                dcount=Count('policy_id'))
            for dates in data:
                print(dates['month'].strftime("%B"))
                lis1.append({"month": dates['month'].strftime("%B"), "count": dates['dcount']})
            return Response(lis1)
        except Policy.DoesNotExist:
            return Response({"Data not fount"}, status=status.HTTP_404_NOT_FOUND)
