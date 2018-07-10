import hashlib

def _hash(string):
    return hashlib.sha512(string.encode('utf-8')).hexdigest()

FAMILY_NAME = 'todo'

NAMESPACE = _hash(FAMILY_NAME)[:6] # namespace

PROJECT_METANODE = '0' # tag character defines address type
SPRINT_METANODE = '1'
TODO_TASK = '2'


def make_task_address(project_name,sprint,task_name,stage):
    return (
        NAMESPACE
        + TODO_TASK
        + _hash(project_name)[:47]
        + sprint
        + _hash(task_name)
        + stage
    )

def make_project_node_address(project_name):
    return (
        NAMESPACE
        + PROJECT_METANODE
        + _hash(project_name)[:47]
        + ('0'*15)
    )

def make_sprint_node_address(project_name,sprint):
    return (
        NAMESPACE
        + SPRINT_METANODE
        + _hash(project_name)[:47]
        + sprint
        + ('0'*13)
    )

