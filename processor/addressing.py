import hashlib

def _hash(string):
    return hashlib.sha512(string.encode('utf-8')).hexdigest()

FAMILY_NAME = 'todo'

NAMESPACE = _hash(FAMILY_NAME)[:6] # namespace

TODO_ITEM = '0' # tag character defines address type
METANODE = '1'

def make_item_address(project_name,sprint,task_name,stage):
    return (
        NAMESPACE
        + TODO_ITEM
        + _hash(project_name)[:47]
        + sprint
        + _hash(task_name)
        + stage
    )