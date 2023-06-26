from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput

from .models import *

class NewsFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postCategory__name',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='все',
    )

    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='lt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type':'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'text': ['icontains'],
        }