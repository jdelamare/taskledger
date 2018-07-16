import hashlib

def _hash(string):
    return hashlib.sha512(string.encode('utf-8')).hexdigest()

FAMILY_NAME = 'todo'

NAMESPACE = _hash(FAMILY_NAME)[:6] # namespace

PROJECT_METANODE = '00' # tag character defines address type
TODO_TASK = '01'


def make_task_address(project_name,task_name):
    return (
        NAMESPACE                   # 6
        + TODO_TASK                 # 2
        + _hash(project_name)[:48]  # 48
        + _hash(task_name)[:14]     # 14
    )

def make_project_node_address(project_name):
    return (
        NAMESPACE
        + PROJECT_METANODE
        + _hash(project_name)[:47]
        + ('0'*15)
    )
