from flask import Flask, request, jsonify, Response, send_file, make_response, url_for

import db_mgmt
import miscmisc
import game

import os
import datetime
import hashlib



app = Flask(__name__, static_url_path=os.path.join(os.getcwd(), '../frontEnd/'))

def show_img(src):
	return "<IMG SRC=\'/icons/{0}\'/>".format(src)
def link_wrap_ip(ip):
	return "<A HREF=\'{0}\'>{1}</A>".format(url_for('show_user', ip=ip), ip)
maps = {'icon' : show_img, 'ip': link_wrap_ip, 'groper': link_wrap_ip, 'gropee': link_wrap_ip}

@app.route('/')
def game():
	return app.send_static_file('game.html')
	#return open('../frontEnd/game.html').read()

@app.route("/clear_and_seed_db")
def clear_and_seed_db():
	db_mgmt.db_init()
	db_mgmt.db_seed()

	return	"<div>Done.</div><p/><div>" + \
			db_mgmt.generate_HTML_table(db_mgmt.get_query_results("SELECT * FROM players"), maps=maps) + \
			"</div><p/><div>" + \
			db_mgmt.generate_HTML_table(db_mgmt.get_query_results("SELECT * FROM gropes"), maps=maps) + \
			"</div>"

@app.route("/clear_db")
def reset_db():
	db_mgmt.db_init()
	return "Ok. Done. What do you want?", 200

@app.route("/icons/<filename>")
def serve_icon(filename):
	try:
		file_path = '../frontEnd/icons/{0}'.format(filename)

		#etag = miscmisc.file_sha1hash(file_path)

		response = send_file(file_path, mimetype="image/png", as_attachment=False, attachment_filename=None, add_etags=True, cache_timeout=None, conditional=False)
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
		return send_file('../frontEnd/js/{0}'.format(filename), mimetype="application/javascript", as_attachment=False, attachment_filename=None, add_etags=True, cache_timeout=None, conditional=False)
	except Exception:
		return "Not Found. (Really... I tried...)", 404

@app.route("/get_my_ip")
def get_my_ip():
	return jsonify({'ip': request.remote_addr}), 200

@app.route("/show_users")
def show_users():
	query_results = db_mgmt.get_query_results("SELECT * FROM players")
	return db_mgmt.generate_HTML_table(query_results, maps=maps), 200

@app.route("/game_state")
def game_state():
	ret1 = db_mgmt.query_results_to_list_of_dicts(db_mgmt.get_query_results("SELECT * FROM players"))
	ret2 = db_mgmt.query_results_to_list_of_dicts(db_mgmt.get_query_results("SELECT * FROM game_state"))
	return jsonify({'players': ret1, 'game': ret2}), 200

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

	query_results = db_mgmt.get_query_results("SELECT * FROM players where ip=\'{0}\'".format(ip))
	s = db_mgmt.generate_HTML_table(query_results, maps=maps)

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