# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Response, send_file, make_response, url_for

import db_mgmt
import miscmisc
import game

import os
import datetime
import hashlib
import random

#KING_B0DH1_PA55W0RD = "BP,YMHaMD,AtPaGBDoyK"
KING_B0DH1_PA55W0RD = "itobwywmtbfsflutsdkwyeomputpowiyscitujcituestitiamtycitujcituibsnicfytibstsmmaibtaiwtdibmlmabllycystysmhttatlccetytiwbhfarifoycitujcituestitiamtycitujcituaesiwimtictibsnicfytibstsmmaibtaiwtdibmlmabllyaikimeuftbikywjlmwsdiyibsnicfytibstsmmaibtaiwtdibmlmabllyibsnicfytitobwywmtbibsnicfytitobwywmtb"

#app = Flask(__name__, static_url_path=os.path.join(os.getcwd(), '../frontEnd/'))
app = Flask(__name__)

def show_img(src):
	return "<IMG SRC=\'/icons/{0}\'/>".format(src)
def link_wrap_ip(ip):
	return "<A HREF=\'{0}\'>{1}</A>".format(url_for('show_user', ip=ip), ip)
maps = {'icon' : show_img, 'ip': link_wrap_ip, 'groper': link_wrap_ip, 'gropee': link_wrap_ip}


def html_dump_queries(queries):
	L = ["".join(["<div><h3>", title, "</h3><p>", db_mgmt.generate_HTML_table(db_mgmt.get_query_results(q), maps=maps), "</p></div><br/>"]) for title, q in queries]
	return "".join(L)

def html_dump():
	tables = ['players', 'game_state', 'messages', 'gropes']
	return html_dump_queries([(tbl, "SELECT * FROM " + tbl) for tbl in tables])


@app.route('/game.html')
def game():
	#return app.send_static_file('game.html')
	return send_file('../frontEnd/game.html')

@app.route('/index.html')
@app.route('/')
def index():
	return send_file('../frontEnd/index.html')

@app.route('/disclaimer.html')
def index1():
	return send_file('../frontEnd/disclaimer.html')

@app.route("/clear_and_seed_db")
def clear_and_seed_db():
	db_mgmt.db_init()
	db_mgmt.db_seed()

	return	"<div>Done.</div><br/>" + html_dump()

@app.route("/clear_db")
def reset_db():
	db_mgmt.db_init()
	return "Ok. Done. What do you want?", 200

@app.route("/icons/<filename>")
def serve_icon(filename):
	try:
		file_path = '../frontEnd/icons/{0}'.format(filename)

		#etag = miscmisc.file_sha1hash(file_path)

		#response = send_file(file_path, mimetype="image/png", as_attachment=False, attachment_filename=None, add_etags=True, cache_timeout=None, conditional=False)
		response = send_file(file_path, mimetype="image/png", as_attachment=False, attachment_filename=None, add_etags=True)
		expiry_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=360000)
		response.headers["Cache-Control"] = "max-age=360000, must-revalidate"
		response.headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

		#response.set_etag(etag)
		return response
	except Exception:
		return "Not Found. (Really... I tried...)", 404

@app.route("/js/<filename>")
def serve_js(filename):
	try:
		#return send_file('../frontEnd/js/{0}'.format(filename), mimetype="application/javascript", as_attachment=False, attachment_filename=None, add_etags=True, cache_timeout=None, conditional=False)
		return send_file('../frontEnd/js/{0}'.format(filename), mimetype="application/javascript", as_attachment=False, attachment_filename=None, add_etags=True)
	except Exception:
		return "Not Found. (Really... I tried...)", 404

@app.route("/get_my_ip")
def get_my_ip():
	return jsonify({'ip': request.remote_addr}), 200

@app.route("/show_all")
def show_all():
	return html_dump()

@app.route("/game_stats")
def game_stats():
	return html_dump_queries(db_mgmt.get_bumpy_queries())

@app.route("/game_state/")
@app.route("/game_state/<ip>")
def game_state(ip = None):
	ret1 = db_mgmt.query_results_to_list_of_dicts(db_mgmt.get_query_results("SELECT * FROM players"))
	ret2 = db_mgmt.query_results_to_list_of_dicts(db_mgmt.get_query_results("SELECT * FROM game_state"))
	d = {'players': ret1, 'game': ret2, 'messages': []}
	if ip is not None:
		d['messages'] = db_mgmt.pull_messages(ip)
	return jsonify(d), 200

@app.route("/set_game_state/")
@app.route("/set_game_state/<blah>/")
@app.route("/set_game_state/<blah>/<password>")
def set_game_state(password = None, blah = ""):
	# Example: http://localhost:8000/set_game_state/p1,,2,5|p2,stuff,2,5.888/<password>
	#          will clear the game_state table and insert rows
	#          ('p1', '', 2, 5) and ('p2', 'stuff', 2, 5.888)

	if password != KING_B0DH1_PA55W0RD:
		# Authentication Failed
		L = [u"запрещено!", u'уходить.', u'Я устал...', u'Я хочу спать...', u'кто ты?', u'я сонный...']
		return L[random.randint(0,len(L)-1)], 403

	anything_done = False
	new_state = []
	success = True

	try:
		new_state = db_mgmt.parse_states(blah)
		anything_done = True
		success = db_mgmt.set_game_state(new_state)
	except Exception:
		success = False

	d = {'success': success, 'anything_done': anything_done, 'game_state': db_mgmt.query_results_to_list_of_dicts(db_mgmt.get_query_results("SELECT * FROM game_state"))}
	return jsonify(d), 200

@app.route("/control/")
@app.route("/control/<password>/")
def control(password = None):
	if password != KING_B0DH1_PA55W0RD:
		# Authentication Failed
		L = [u"запрещено!", u'уходить.', u'Я устал...', u'Я хочу спать...', u'кто ты?', u'я сонный...']
		return L[random.randint(0,len(L)-1)], 403

	return send_file('../frontEnd/control.html')


@app.route("/add_or_update_user/<ip>/<name>/<icon>/<sex>/<race>/<class_>/<min_x_>/<max_x_>/<min_y_>/<max_y_>")
def add_or_update_user(ip, name, icon, sex, race, class_, min_x_, max_x_, min_y_, max_y_):
	ret = {}
	try:
		min_x, max_x, min_y, max_y = int(min_x_), int(max_x_), int(min_y_), int(max_y_)
		ret = db_mgmt.add_or_update_user(ip, name, icon, sex, race, class_, min_x, max_x, min_y, max_y)
	except Exception:
		ret = {'success': False, 'message': 'Bad Input'}
	return jsonify(ret), 200

@app.route("/dump_it_all")
def dump_it_all():
	ret1_tabular = db_mgmt.get_query_results("SELECT * FROM players")
	ret2_tabular = db_mgmt.get_query_results("SELECT * FROM gropes")
	ret1_dod = db_mgmt.query_results_to_list_of_dicts(ret1_tabular)
	ret2_dod = db_mgmt.query_results_to_list_of_dicts(ret2_tabular)
	return jsonify({'as_list_of_dicts': {'players': ret1_dod, 'gropes': ret2_dod}, 'tabularly': {'players': ret1_tabular, 'gropes': ret2_tabular}}), 200
	# Yeah... I could do it more generally, but why...

@app.route("/show_user/<ip>")
def show_user(ip):
	query_results = db_mgmt.get_query_results("SELECT * FROM players WHERE ip=\'{0}\'".format(ip), True)
	return db_mgmt.generate_HTML_table(query_results, maps=maps), 200

@app.route("/move/<ip>/<move>")
def move(ip, move):
	ret = {'success': True}

	move_x = 0
	move_y = 0

	if move.upper() == "LEFT":
		move_x = -1
		move_y = 0
	elif move.upper() == "RIGHT":
		move_x = 1
		move_y = 0
	elif move.upper() == "DOWN":
		move_x = 0
		move_y = -1
	elif move.upper() == "UP":
		move_x = 0
		move_y = 1
	else:
		ret['success'] = False

	#query_results = db_mgmt.get_query_results("SELECT * FROM players where ip=\'{0}\'".format(ip))
	#s = db_mgmt.generate_HTML_table(query_results, maps=maps)

	if ret['success']:
		ret['details'] = db_mgmt.attempt_move_to(ip, move_x, move_y)

		#query_results = db_mgmt.get_query_results("SELECT * FROM players where ip=\'{0}\'".format(ip))
		#s += "<br/><br/><br/>"
		#s += db_mgmt.generate_HTML_table(query_results, maps=maps)
		#s += "<br/><br/><br/>"
		#query_results = db_mgmt.get_query_results("SELECT * FROM messages")
		#s += db_mgmt.generate_HTML_table(query_results, maps=maps)

	#return s, 200
	return jsonify(ret), 200




if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8000, debug=True)
    #app.run(host='0.0.0.0', port=8000)