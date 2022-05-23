import django_filters
from .models import Policy

class PolicyFilter(django_filters.FilterSet):

    class Meta:
        model = Policy
        fields= (
            'id','policy_id','customer_id'
        )