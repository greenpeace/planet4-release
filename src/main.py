import json
import os
from pycircleci.api import Api

CIRCLE_API = 'https://circleci.com/api/v2/project/github/greenpeace/planet4-base/pipeline'
USERNAME = 'greenpeace'
PROJECT = 'planet4-base'
BRANCH = 'main'


def main(request):
    request_json = request.get_json()

    try:
        version = 'v{0}'.format(request_json['version']['name'])
    except KeyError:
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
