import json
import os
import sys
from pycircleci.api import Api

USERNAME = 'greenpeace'
PROJECT = 'planet4-base'
BRANCH = 'main'


def ticket(ticket, fields):
    try:
        status = fields['status']['name']
    except (KeyError, TypeError):
        raise Exception('Not a valid ticket status')

    if status != 'CLOSED':
        sys.exit(0)

    labels = fields['labels']
    if 'FLAG' not in labels:
        sys.exit(0)

    parameters = {
        "ticket": ticket,
        "flag-ticket": True
    }

    return parameters


def release(version):
    parameters = {
        "version": version,
        "promote": True
    }

    return parameters


def main(request):
    request_json = request.get_json()
    version = False

    try:
        version = 'v{0}'.format(request_json['version']['name'])
        parameters = release(version)
    except (KeyError, TypeError):
        pass

    if not version:
        try:
            fields = request_json['issue']['fields']
            parameters = ticket(request_json['issue']['key'], fields)
        except (KeyError, TypeError):
            raise Exception('Not a valid version number or ticket provided')

    circleci = Api(os.getenv('CIRCLE_TOKEN'))

    response = circleci.trigger_pipeline(username=USERNAME,
                                         project=PROJECT,
                                         branch=BRANCH,
                                         params=parameters)

    return json.dumps(response)
