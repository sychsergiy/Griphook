def get_average_services_group_load_chart_data(service_group: str, services: list, time_from: int,
                                               time_until: int):
    # response = send_graphite_request(time_from, time_until, metric_type) # use response from stub

    # converted_multipe_values = MultipleValues(*services)
    return mock_api_response()

def mock_api_response():
    return {
        'parent': {
            'target': 'test',
            'value': 123
        },
        'children': []
    }