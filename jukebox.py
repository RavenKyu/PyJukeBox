import os
import threading
import random
import argparse
from flask import Flask


from subprocess import Popen

from modules.users import userlist
from modules.playlist import playlist

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

app.register_blueprint(userlist, url_prefix='/users')
app.register_blueprint(playlist, url_prefix='/playlist')



#
# ################################################################################
# class EndOfList(Exception):
#     pass


# ################################################################################
# class PlayList(list):
#     def __init__(self):
#         list.__init__(self)
#         self.cur_idx = 0
#         self.shuffle = False
#         self.repeat = False
#
#     # ==========================================================================
#     def __iter__(self):
#         self.cur_idx = 0
#         return self
#
#     # ==========================================================================
#     def current_item(self):
#         return self[self.cur_idx]
#
#     # ==========================================================================
#     def shuffle(self):
#         random.shuffle(self)
#
#     # ==========================================================================
#     def __next__(self):
#         if self.cur_idx >= len(self) - 1:
#             if self.repeat:
#                 self.cur_idx = 0
#             else:
#                 raise StopIteration
#         cur_idx = self.cur_idx
#         self.cur_idx += 1
#         return self[cur_idx]
#
#     # ==========================================================================
#     def next_track(self):
#         if self.cur_idx >= len(self) - 1:
#             raise EndOfList
#         self.cur_idx += 1
#         return self[self.cur_idx]
#
#     # ==========================================================================
#     def previous_track(self):
#         if self.cur_idx - 1 <= len(self) - 1:
#             return
#         self.cur_idx -= 1
#         return self[self.cur_idx]




# `


# ################################################################################
# @app.route('/playlist', methods=['GET', 'PUT'])
# def playlist():
#     if request.accept_mimetypes == 'application/json':
#         return jsonify({'data': play_list})
#     else:
#         return render_template('userlist.html')
#
# @app.route('/playlist', methods=['PUT'])
# def playlist():
#     url = request.args.get('url')
#     play_list.append(url)
#     return jsonify({'data': play_list})


# th = Execution()
# th.daemon = True
# th.start()


# ################################################################################
# @app.route('/play')
# def play():
#     order_number = request.args.get('order_num')
#     th.play_list.cur_idx = int(order_number)
#     url = th.play_list.current_item()
#     th.action = 'play'
#     th.play(url)
#     return jsonify(**{'result': True})
#
#
# ################################################################################
# @app.route('/stop')
# def stop():
#     th.action = 'stop'
#     th.stop()
#     return jsonify(**{'result': True})
#
#
# ################################################################################
# @app.route('/next')
# def next_track():
#     url = th.play_list.next_track()
#     th.play(url)
#     return jsonify(**{'result': True})
#
#
# ################################################################################
# @app.route('/previous')
# def previous_track():
#     url = th.play_list.previous_track()
#     th.play(url)
#     return jsonify(**{'result': True})



################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", type=bool)
    argspec = parser.parse_args()
    if argspec.reset:
        drop_create_all()

    app.run(host='0.0.0.0', debug=True)
    # th.join()
