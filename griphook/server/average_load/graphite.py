from griphook.api.graphite.target import MultipleValues


def get_average_server_load_chart_data(server: str, services: list, time_from: int, time_until: int):
    # converted_multipe_values = MultipleValues(*services)
    # response = send_graphite_request(time_from, time_until, metric_type) # use response from stub
    return mock_api_response()


def get_average_services_group_load_chart_data(service_group: str, services: list, time_from: int,
                                               time_until: int):
    # response = send_graphite_request(time_from, time_until, metric_type) # use response from stub

    # converted_multipe_values = MultipleValues(*services)
    return mock_api_response()


def get_average_service_load_chart_data(service: str, services: list, time_from: int, time_until: int):
    # converted_multipe_values = MultipleValues(*services)
    # response = send_graphite_request(time_from, time_until, metric_type) # use response from stub
    return mock_api_response()


def mock_api_response():
    from griphook.server.average_load.mock import result
    return result
