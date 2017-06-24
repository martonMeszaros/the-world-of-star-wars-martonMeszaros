import json
import requests

import vote_data_manager


def new_vote(planet_id):
    vote_data_manager.new_vote(planet_id)
    return ''


def get_votes():
    votes = vote_data_manager.get_votes()
    votes_dict = {
        'results': []
    }
    for vote in votes:
        response = requests.get('http://swapi.co/api/planets/{}'.format(vote[0])).json()
        votes_dict['results'].append({
            'planet': response['name'],
            'count': vote[1]
        })
    return json.dumps(votes_dict)
