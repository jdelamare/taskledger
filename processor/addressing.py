# MIT License
#
# Copyright (c) 2018 Nicholas Springer & Jeffrey De La Mare
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import hashlib

def _hash(string):
    return hashlib.sha512(string.encode('utf-8')).hexdigest()

FAMILY_NAME = 'todo'

NAMESPACE = _hash(FAMILY_NAME)[:6] # namespace

PROJECT_METANODE = '00' # tag character defines address type
SPRINT_METANODE = '01'
TODO_TASK = '02'


def make_task_address(project_name,sprint,task_name):
    return (
        NAMESPACE
        + TODO_TASK
        + _hash(project_name)[:47]
        + str(sprint)
        + _hash(task_name)[:14]
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
        + str(sprint)
        + ('0'*14)
    )

