import json
import os
from pycircleci.api import Api

USERNAME = 'greenpeace'
PROJECT = 'planet4-base'
BRANCH = 'main'


def main(request):
    request_json = request.get_json()

    try:
        version = 'v{0}'.format(request_json['version']['name'])
    except (KeyError, TypeError):
        raise Exception('Version number was not provided')

    circleci = Api(os.getenv('CIRCLE_TOKEN'))

    parameters = {
        "version": version,
        "promote": True
    }

    response = circleci.trigger_pipeline(username=USERNAME,
                                         project=PROJECT,
                                         branch=BRANCH,
                                         params=parameters)

    return json.dumps(response)
