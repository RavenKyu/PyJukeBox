import argparse
import json

from config import app, db, api
from models import User, UserPlayList, UserPlayListIndex
from modules.users import api as userlist
from modules.playlist import api as playlist

app = app
api = api
db.init_app(app)
db.create_all()

api.add_namespace(userlist, path='/users')
api.add_namespace(playlist, path='/users')



def insert_dummy_data(data):
    global db
    data = json.load(data)

    for user in data:
        u = User(user['name'], user['password'], user['email'])
        db.session.add(u)
        db.session.flush()

        playlist_index_data = list()
        for pl in user['playlist']:
            playlist_index = UserPlayListIndex(pl['name'])
            db.session.add(playlist_index)
            db.session.flush()

            playlist_data = list()
            for music in pl['musics']:
                m = UserPlayList(
                    music['title'], music['url'], music['description'])
                db.session.add(m)
                playlist_data.append(m)
            playlist_index.user_play_list = playlist_data
            playlist_index_data.append(playlist_index)
        u.user_play_list_index = playlist_index_data
        db.session.flush()
        db.session.commit()
        print(u)


################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", type=bool)
    parser.add_argument("--insert-dummy",
                        type=argparse.FileType('r', encoding='utf-8-sig'))

    argspec = parser.parse_args()
    # if argspec.reset:
    #     drop_create_all()
    if argspec.insert_dummy:
        insert_dummy_data(argspec.insert_dummy)

    app.run(host='0.0.0.0', debug=True)

