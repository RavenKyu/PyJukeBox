from flask import Flask, request, jsonify
from subprocess import Popen
import threading
import random


app = Flask(__name__)


################################################################################
class EndOfList(Exception):
    pass


################################################################################
class PlayList(list):
    def __init__(self):
        list.__init__(self)
        self.cur_idx = 0
        self.shuffle = False
        self.repeat = False

    # ==========================================================================
    def __iter__(self):
        self.cur_idx = 0
        return self

    # ==========================================================================
    def current_item(self):
        return self[self.cur_idx]

    # ==========================================================================
    def shuffle(self):
        random.shuffle(self)

    # ==========================================================================
    def __next__(self):
        if self.cur_idx >= len(self) - 1:
            if self.repeat:
                self.cur_idx = 0
            else:
                raise StopIteration
        cur_idx = self.cur_idx
        self.cur_idx += 1
        return self[cur_idx]

    # ==========================================================================
    def next_track(self):
        if self.cur_idx >= len(self) - 1:
            raise EndOfList
        self.cur_idx += 1
        return self[self.cur_idx]

    # ==========================================================================
    def previous_track(self):
        if self.cur_idx - 1 <= len(self) - 1:
            return
        self.cur_idx -= 1
        return self[self.cur_idx]


play_list = PlayList()


################################################################################
class Execution(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_order_number = 0
        self.cmd = None
        self.proc = None
        self.action = 'stop'

    # ==========================================================================
    def play(self, url):
        self.stop()
        cmd = "exec mpv \"$(yturl '{}')\"".format(url)
        self.proc = Popen(cmd, shell=True)
        self.action = 'play'
        return True

    # ==========================================================================
    def stop(self):
        if self.proc is None:
            return
        if self.proc.returncode is not None:
            return
        self.proc.kill()
        self.proc = None
        self.action = 'stop'

    # ==========================================================================
    def run(self):
        while self.action == 'play':
            if self.proc is None:
                url = play_list.current_item()
                self.play(url)
                play_list.next_track()
            if not play_list.repeat:
                break


################################################################################
@app.route('/playlist', methods=['GET', 'PUT'])
def playlist():
    if request.method == 'GET':
        pass
    else:
        url = request.args.get('url')
        play_list.append(url)
        print(play_list)
    return jsonify(**{'data': play_list})


################################################################################
@app.route('/play')
def play():
    order_number = request.args.get('order_num')
    play_list.cur_idx = int(order_number)
    url = play_list.current_item()
    th.action = 'play'
    th.play(url)
    return jsonify(**{'result': True})


################################################################################
@app.route('/stop')
def stop():
    th.action = 'stop'
    th.stop()
    return jsonify(**{'result': True})


################################################################################
@app.route('/next')
def next_track():
    url = play_list.next_track()
    th.play(url)
    return jsonify(**{'result': True})


################################################################################
@app.route('/previous')
def previous_track():
    url = play_list.previous_track()
    th.play(url)
    return jsonify(**{'result': True})


th = Execution()


################################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
