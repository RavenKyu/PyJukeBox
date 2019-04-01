import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.sqlite3db import User, UserPlayList, UserPlayListIndex, db as DB

################################################################################
class TestUnit (unittest.TestCase):
    """
    Test Unit for Locate Image
    """

    # ==========================================================================
    def setUp(self):
        self.db = DB
        DB.create_all()

    # ==========================================================================
    def tearDown(self):
        self.db.drop_all()

    # ==========================================================================
    def test_100(self):
        user = User(name='raven',
                    password='1234',
                    email='hong18s@gmail.com',)

        self.db.session.add(user)
        self.db.session.commit()
        self.assertEqual('raven', User.query.first().name)

    # ==========================================================================
    def test_110(self):
        user = User(name='raven',
                    password='1234',
                    email='hong18s@gmail.com',)

        playlist = UserPlayListIndex(name="Classic")
        user.user_play_list_index = [playlist]

        self.db.session.add(user)
        self.db.session.commit()
        playlist = User.query.first().user_play_list_index[0]
        self.assertEqual('Classic', playlist.name)
        u = playlist.user
        self.assertEqual('raven', u.name)

    # ==========================================================================
    def test_120(self):
        user = User(name='raven',
                    password='1234',
                    email='hong18s@gmail.com',)

        playlist = UserPlayListIndex(name="Classic")
        musics = [
            UserPlayList("Jaco Pastrious - Chicken",
                         "https://www.youtube.com/watch?v=TgntkGc5iBo&list=RDT"
                         "gntkGc5iBo&start_radio=1",
                         "Jaco"),
            UserPlayList("Weather Report - Teen Town",
                         "https://www.youtube.com/watch?v=TgntkGc5iBo&list=RDT"
                         "gntkGc5iBo&start_radio=1",
                         "WR")
        ]
        playlist.play_list_index = musics
        user.user_play_list_index = [playlist]

        self.db.session.add(user)
        self.db.session.commit()
        playlist = User.query.first().user_play_list_index[0]
        print(playlist.play_list_index)
        self.assertEqual('Classic', playlist.name)
        u = playlist.user
        self.assertEqual('raven', u.name)