# Introduction

This is a little game (with a poorly thought out title) that was (will be) used to demonstrate a working Python app to students of the Masters of Business Analytics program at the National University of Singapore at the beginnning of the 2014/2015 Academic Year.

In what passes for a multiplayer game, players walk around and collect coins. They get to view a leaderboard with scores and are amused by various unusual sounds played when things happen (collisions occur/coins are collected). Meanwhile, data on their actions is being recorded on the sly... (Think Google with locations, banks with payments and...)

Aside from being a (shoddily built) Python web app, this may be used to illustrate exploratory data analysis (see */dump_it_all* and some EDA of it in */game_stats*), the capture of location data (see */high_fidelity_records* and */high_fidelity_records_html*).

There is even a client bot that may be used to illustrate automation at */game_bot*. (A password is needed except for whoever can access the server via **localhost**.)


# Installation

Copy all files.

Make sure you have *Python 2.7* (we use 2.7.6) and *PostgreSQL* (we use 9.3.3).

(Use *pip* to...) Install *psycopg2* (we use 2.5.2), *flask* (we use 0.10.1) and *waitress* (we use 0.8.9).

# Usage

In the /backEnd folder, run **python bum.py**. The game should be served on port *8000* (by default).

One may access the game server from the **localhost** interface may forgo passwords and control the game via *localhost:8000/control*. A game controller is needed to ensure that coins do get generated (a lot of stuff is done on the front-end). Most of the stuff described may be accessed from */control*.

Passwords are at the top of */backEnd/bum.py*. (All passwords are first characters of song lyrics. Guess which.)

# Blame

Blame for this abomination may be assigned to Bodhisatta Barman Roy (thebbroy@gmail.com) and Jeremy Chen (convexset@gmail.com)

