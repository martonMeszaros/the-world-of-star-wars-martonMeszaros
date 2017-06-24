import datetime

from flask import session

from db_connection import connect_to_db
import users_data_manager


@connect_to_db
def new_vote(planet_id):
    user_id = users_data_manager.get_user_by_username(session['user'])[0][0]
    return (
        '''
        INSERT INTO planet_votes
            (planet_id, user_id, submission_time)
        VALUES
            (%s, %s, %s);
        ''',
        [planet_id, user_id, datetime.datetime.now()]
    )
