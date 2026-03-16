
class FilterQueryMixin:
    def filter_query(self, queryset, filters):
        for field, value in filters.items():
            if value is not None:
                queryset = queryset.filter(**{field: value})
        return queryset
