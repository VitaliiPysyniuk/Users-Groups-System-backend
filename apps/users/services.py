from rest_framework.exceptions import ParseError

from .models import UsedModel

AVAILABLE_FILTER_FUNCTIONS = ('email__endswith', 'email__startswith', 'username__startswith', 'is_admin',
                              'created_at__date', 'created_at__date__lt', 'created_at__date__gt', 'groups__in')


def parse_users_query_params(query_params: dict) -> dict:
    """
    Parses query parameters.

    Processes every query parameter, checks if the query parameter is
    available to use for filtering if not available query parameter
    was used raises an exception, casts bool values from string to
    bool. If the groups__in query parameter was set filters all users
    who belong to these groups.

    Parameters:
    query_params (dict): Query parameters before parsing

    Returns:
    dict: Parsed query parameters
    """
    parsed_query_params = dict()

    for filter_function, filter_input in query_params.items():
        if filter_function not in AVAILABLE_FILTER_FUNCTIONS:
            raise ParseError(detail=f'Invalid filter function: {filter_function}')
        else:
            if filter_input == 'True':
                parsed_query_params[filter_function] = True
            elif filter_input == 'False':
                parsed_query_params[filter_function] = False
            elif filter_function == 'groups__in':
                groups = [int(group) for group in filter_input.split(',')]
                parsed_query_params['id__in'] = UsedModel.objects.filter(groups__in=groups).distinct()
            else:
                parsed_query_params[filter_function] = filter_input

    return parsed_query_params
