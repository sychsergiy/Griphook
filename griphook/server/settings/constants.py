# exceptions text for project, team, server, cluster API
EXC_FIELD_IS_REQUIRED = 'The field /{}/ is required'

# exceptions text for validators
EXC_LENGTH_TITLE_NOT_VALID = 'Length title {} not valid'

# lists of required fields for the API
PARAMETERS_PROJECT_TEAM = ['id', 'title']
PARAMETERS_SERVER_CLUSTER_CPU_PRICE = ['id', 'cpu_price']
PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE = ['id', 'memory_price']
PARAMETERS_ATTACH_PROJECT = ['project_id', 'services_group_id']
PARAMETERS_ATTACH_TEAM = ['team_id', 'services_group_id']
PARAMETERS_DETACH_PROJECT_TEAM = ['services_group_id']
