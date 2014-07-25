from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import url_for
import db_mgmt
import os

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
	return "Ok."

@app.route("/icons/<filename>")
def serve_icon(filename):
	try:
		data = open('../frontEnd/icons/{0}'.format(filename)).read()
		return Response(response=data, status=200, headers=None, mimetype='image/png', content_type=None, direct_passthrough=False)
	except IOError as exc:
		return str(exc)

@app.route("/js/<filename>")
def serve_js(filename):
	try:
		return open('../frontEnd/js/{0}'.format(filename)).read()
	except IOError as exc:
		return str(exc)

@app.route("/get_my_ip")
def get_my_ip():
	return jsonify({'ip': request.remote_addr}), 200

@app.route("/show_users")
def show_users():
	query_results = db_mgmt.get_query_results("SELECT * FROM players")
	return db_mgmt.generate_HTML_table(query_results, maps=maps)

@app.route("/show_user/<ip>")
def show_user(ip):
	query_results = db_mgmt.get_query_results("SELECT * FROM players WHERE ip=\'{0}\'".format(ip), True)
	return db_mgmt.generate_HTML_table(query_results, maps=maps)

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8000, debug=True)
    #app.run(host='0.0.0.0', port=8000)