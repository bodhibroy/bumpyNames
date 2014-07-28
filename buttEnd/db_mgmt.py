import psycopg2
import random
import sys

from game import game_messages

def db_connection():
	return psycopg2.connect(host='localhost', port=5432, database='BumpyMaps', user='BumpyMaps', password='BumpBumpBump') 

def db_init(top_gg_limit = 5, top_avoider_limit = 10):
    conn = db_connection() 
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS players CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS gropes CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS messages CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS game_state CASCADE;")
    
    cursor.execute("""
        CREATE TABLE players
        (
          ip inet NOT NULL,
          name varchar(20),
          icon varchar(255),
          sex varchar(10),
          race varchar(20),
          class varchar(30),
          location_x integer,
          location_y integer,
          burns integer DEFAULT 0,
          moves integer DEFAULT 0,
          CONSTRAINT ip PRIMARY KEY (ip)
        );
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE TABLE gropes
        (
          groper inet NOT NULL,
          gropee inet NOT NULL,
          count integer DEFAULT 0,
          CONSTRAINT gropee FOREIGN KEY (gropee)
              REFERENCES players (ip) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE NO ACTION,
          CONSTRAINT groper FOREIGN KEY (groper)
              REFERENCES players (ip) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE NO ACTION
        );
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE TABLE messages
        (
          ip inet NOT NULL,
          message integer,
          intval1 integer,
          intval2 integer,
          intval3 integer,
          intval4 integer,
          strval varchar(50),
          CONSTRAINT ip FOREIGN KEY (ip)
              REFERENCES players (ip) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE NO ACTION
        );
        """.format(top_gg_limit, top_avoider_limit))
   
    cursor.execute("""
        CREATE TABLE game_state
        (
          property varchar(50),
          str_val varchar(50),
          int_val integer,
          dec_val decimal
        );
        """.format(top_gg_limit, top_avoider_limit))
    
    cursor.execute("""
        CREATE OR REPLACE VIEW groper_grope_counts_ AS
            SELECT gropes.groper AS groper_ip, SUM(gropes.count) AS grope_count
                FROM gropes
                JOIN players ON (gropes.groper = players.ip)
                GROUP BY gropes.groper;
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW gropee_grope_counts_ AS
            SELECT gropes.gropee AS gropee_ip, SUM(gropes.count) AS grope_count
                FROM gropes
                JOIN players ON (gropes.gropee = players.ip)
                GROUP BY gropes.gropee;
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW groper_grope_counts AS
            SELECT players.name AS name, gropes_base.groper_ip AS ip, gropes_base.grope_count AS grope_count, players.sex AS sex, players.race AS race, players.class AS class
                FROM groper_grope_counts_ AS gropes_base
                INNER JOIN players ON (gropes_base.groper_ip = players.ip);
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW gropee_grope_counts AS
            SELECT players.name AS name, gropes_base.gropee_ip AS ip, gropes_base.grope_count AS grope_count, players.sex AS sex, players.race AS race, players.class AS class
                FROM gropee_grope_counts_ AS gropes_base
                INNER JOIN players ON (gropes_base.gropee_ip = players.ip);
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW top_groper_grope_counts AS
            SELECT * FROM groper_grope_counts
                ORDER BY grope_count DESC, name
                LIMIT {0};
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW top_gropee_grope_counts AS
            SELECT * FROM gropee_grope_counts
                ORDER BY grope_count DESC, name
                LIMIT {0};        
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW least_gropey_grope_counts AS
            SELECT * FROM groper_grope_counts
                ORDER BY grope_count
                LIMIT {1};
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW least_groped_grope_counts AS
            SELECT * FROM gropee_grope_counts
                ORDER BY grope_count
                LIMIT {1};
        """.format(top_gg_limit, top_avoider_limit))

    cursor.execute("""
        CREATE OR REPLACE VIEW grope_pairs AS
            SELECT players1.name AS groper, players2.name AS gropee, gropes.count AS grope_count
                FROM gropes
                INNER JOIN players AS players1 ON (gropes.groper = players1.ip)
                INNER JOIN players AS players2 ON (gropes.gropee = players2.ip);
        """.format(top_gg_limit, top_avoider_limit))

    conn.commit()
    conn.close()


def db_seed(num_rnd = 10, p_g = 0.25, p_gv1 = 0.2, p_gv2 = 0.35):
    conn = db_connection() 
    cursor = conn.cursor()
    
    def rnd_icon():
        L0 = ["AnimalIcons_Elephant_32x32.png", "Animal_Icons_bull.png", "Animal_Icons_duck.png", "Animal_Icons_lion.png", "Animal_Icons_shark.png", "AnimalIcons_Giraffe_32x32.png", "Animal_Icons_bulldog.png", "Animal_Icons_eagle.png", "Animal_Icons_monkey.png", "Animal_Icons_sheep.png", "AnimalIcons_Gorilla_32x32.png", "Animal_Icons_butterfly.png", "Animal_Icons_elephant.png", "Animal_Icons_moose.png", "Animal_Icons_snake.png", "AnimalIcons_Lion_32x32.png", "Animal_Icons_cat.png", "Animal_Icons_fish.png", "Animal_Icons_mouse.png", "Animal_Icons_tiger.png", "AnimalIcons_Zebra_32x32.png", "Animal_Icons_chicken.png", "Animal_Icons_fox.png", "Animal_Icons_owl.png", "Animal_Icons_turkey.png", "Animal_Icons_alligator.png", "Animal_Icons_cow.png", "Animal_Icons_frog.png", "Animal_Icons_panda.png", "Animal_Icons_turtle.png", "Animal_Icons_ant.png", "Animal_Icons_crab.png", "Animal_Icons_giraffe.png", "Animal_Icons_penguin.png", "Animal_Icons_wolf.png", "Animal_Icons_bat.png", "Animal_Icons_crocodile.png", "Animal_Icons_gorilla.png", "Animal_Icons_pig.png", "Animal_Icons_bear.png", "Animal_Icons_deer.png", "Animal_Icons_hippo.png", "Animal_Icons_rabbit.png", "Animal_Icons_bee.png", "Animal_Icons_dog.png", "Animal_Icons_horse.png", "Animal_Icons_rhino.png", "Animal_Icons_bird.png", "Animal_Icons_donkey.png", "Animal_Icons_insect.png", "Animal_Icons_rooster.png"];
        #L = ["./icons/{0}".format(s) for s in L0]
        L = L0
        return L[random.randint(0,len(L)-1)]
    
    def rnd_sex():
        L = ['Male', 'Female', 'Female PhD']
        return L[random.randint(0,len(L)-1)]
    
    def rnd_race():
        L = ['Human', 'Elf', 'Dwarf', 'Orc', 'Gnome', 'Otter']
        return L[random.randint(0,len(L)-1)]
    
    def rnd_class():
        L = ['Bee Keeper', 'Snake Charmer', 'Hog Farmer', 'Baby Elephant Wrangler', 'XMM']
        return L[random.randint(0,len(L)-1)]
    
    cursor.execute("""INSERT INTO players VALUES ('10.0.0.1', 'Big Bodhi', '{0}', 'Male', 'Otter', 'Chef', '0', '0', 0);""".format(rnd_icon()))
    cursor.execute("""INSERT INTO players VALUES ('10.0.0.2', 'Zen Chia Zhong Da', '{0}', 'Male', 'Gnome', 'XMM Herder', '0', '3', 1);""".format(rnd_icon()))

    base_people = """INSERT INTO players VALUES ('10.0.0.{0}', 'Player {1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8});""" 
    
    for k in range(num_rnd):
        cursor.execute(base_people.format(101+k, k+1, rnd_icon(), rnd_sex(), rnd_race(), rnd_class(), random.randint(0,25), random.randint(0,25), random.randint(0,5)))

    if random.random() <= p_gv1:
        cursor.execute("INSERT INTO gropes VALUES ('10.0.0.1', '10.0.0.2', {0});".format(random.randint(1,10)))
    if random.random() <= p_gv2:
        cursor.execute("INSERT INTO gropes VALUES ('10.0.0.2', '10.0.0.1', {0});".format(random.randint(1,10)))

    for k1 in range(num_rnd):
        if random.random() <= p_gv1:
            cursor.execute("INSERT INTO gropes VALUES ('10.0.0.1', '10.0.0.{0}', {1});".format(101+k1,random.randint(1,10)))
        if random.random() <= p_gv2:
            cursor.execute("INSERT INTO gropes VALUES ('10.0.0.2', '10.0.0.{0}', {1});".format(101+k1,random.randint(1,10)))
        if random.random() <= p_g:
            cursor.execute("INSERT INTO gropes VALUES ('10.0.0.{0}', '10.0.0.1', {1});".format(101+k1,random.randint(1,10)))
        if random.random() <= p_g:
            cursor.execute("INSERT INTO gropes VALUES ('10.0.0.{0}', '10.0.0.2', {1});".format(101+k1,random.randint(1,10)))
            
        for k2 in range(num_rnd):
            if k1 == k2:
                continue
            else:
                if random.random() <= p_g:
                    cursor.execute("INSERT INTO gropes VALUES ('10.0.0.{0}', '10.0.0.{1}', {2});".format(101+k1,101+k2,random.randint(1,12)))
    conn.commit()
    conn.close()
    


def quick_query(q):
    conn = None
    ret_code = 0
    try:
        conn = db_connection() 
        cursor = conn.cursor()
        cursor.execute(q)
        conn.commit()
    except psycopg2.DatabaseError, e:
        ret_code = -1
    finally:
        if conn:
            conn.close()
        return ret_code

def get_query_results(query, trim = False):
    conn = None
    ret = []
    try:
        conn = db_connection() 
        cursor = conn.cursor()
        cursor.execute(query)
        cols = [cn[0] for cn in cursor.description]
        for row in cursor:
            this_row = [s.strip() if hasattr(s, 'strip') else s for s in row] if trim else row
            ret.append(this_row)
    
        conn.close()
        return {'cols': cols, data: ret}
           
    except psycopg2.DatabaseError, e:
        pass
        
    finally:
        
        if conn:
            conn.close()
            return {'cols': cols, 'data': ret}
        else:
            return None


def get_table(tbl_name, trim = False):
    return get_query_results("SELECT * FROM %s" % tbl_name, trim)

def query_results_to_list_of_dicts(qresults):
    if qresults is None:
        return None
    ret = []
    for row in qresults['data']:
        ret.append(dict(zip(qresults['cols'], row)))
    return ret

def get_table_listOdicts(tbl_name, trim = False):
    return query_results_to_list_of_dicts(get_table(tbl_name, trim))



def get_bumpy_queries():
	queries = {}

	queries['Top Grope Pairs'] = "SELECT * FROM grope_pairs ORDER BY grope_count DESC LIMIT 10;"


	queries['Top Grope Buddies'] = """
	SELECT
	        CASE WHEN gp1.groper < gp1.gropee THEN gp1.groper
	            ELSE gp1.gropee
	        END AS person_one,
	        CASE WHEN gp1.groper < gp1.gropee THEN gp1.gropee
	            ELSE gp1.groper
	        END AS person_two,
	        (COALESCE(gp1.grope_count,0)+COALESCE(gp2.grope_count,0)) AS gropes_exchanged,
	        ABS(COALESCE(gp1.grope_count,0)-COALESCE(gp2.grope_count,0)) / (0.0 + COALESCE(gp1.grope_count,0)+COALESCE(gp2.grope_count,0)) AS asymmetry
	    FROM grope_pairs AS gp1
	    LEFT JOIN grope_pairs AS gp2
	        ON (gp1.groper = gp2.gropee AND gp2.groper = gp1.gropee)
	    WHERE (gp2.groper IS NULL OR gp1.groper < gp1.gropee)
	    ORDER BY gropes_exchanged DESC, person_one, person_two
	    LIMIT 10
	;"""


	queries['Top Gropers'] = "SELECT * FROM top_groper_grope_counts;"


	queries['Top Gropees'] = "SELECT * FROM top_gropee_grope_counts;"


	queries['Polite Society'] = "SELECT * FROM least_gropey_grope_counts;"


	queries['Sexual Predator Awareness Role Models'] = "SELECT * FROM least_groped_grope_counts;"


	queries['Star Crossed Pairs (Male Gropers)'] = """
	SELECT players1.name as groper_name, players2.name as gropee_name
	    FROM players AS players1
	    JOIN players AS players2 ON (players1.ip != players2.ip AND players1.sex != players2.sex)
	        LEFT JOIN gropes ON (players1.ip = gropes.groper AND players2.ip = gropes.gropee)
	    WHERE players1.sex = 'Male' AND COALESCE(gropes.count,0) = 0
	    ORDER BY groper_name, gropee_name;
	"""


	queries['Star Crossed Pairs (Female Gropers)'] = """
	SELECT players1.name as groper_name, players2.name as gropee_name
	    FROM players AS players1
	    JOIN players AS players2 ON (players1.ip != players2.ip AND players1.sex != players2.sex)
	        LEFT JOIN gropes ON (players1.ip = gropes.groper AND players2.ip = gropes.gropee)
	    WHERE players1.sex = 'Female' AND COALESCE(gropes.count,0) = 0
	    ORDER BY groper_name, gropee_name;
	"""


	queries['Average/Max/Min Groper Gropes by Sex'] = """
	SELECT sex, SUM(grope_count), COUNT(grope_count), AVG(grope_count), MIN(grope_count), MAX(grope_count)
	    FROM groper_grope_counts GROUP BY sex ORDER BY sex;
	"""


	queries['Average/Max/Min Groper Gropes by Race'] = """
	SELECT race, SUM(grope_count), COUNT(grope_count), AVG(grope_count), MIN(grope_count), MAX(grope_count)
	    FROM groper_grope_counts GROUP BY race ORDER BY race;
	"""


	queries['Average/Max/Min Groper Gropes by Class'] = """
	SELECT class, SUM(grope_count), COUNT(grope_count), AVG(grope_count), MIN(grope_count), MAX(grope_count)
	    FROM groper_grope_counts GROUP BY class ORDER BY class;
	"""


	queries['Average/Max/Min Gropee Gropes by Sex'] = """
	SELECT sex, SUM(grope_count), COUNT(grope_count), AVG(grope_count), MIN(grope_count), MAX(grope_count)
	    FROM gropee_grope_counts GROUP BY sex ORDER BY sex;
	"""


	queries['Average/Max/Min Gropee Gropes by Race'] = """
	SELECT race, SUM(grope_count), COUNT(grope_count), AVG(grope_count), MIN(grope_count), MAX(grope_count)
	    FROM gropee_grope_counts GROUP BY race ORDER BY race;
	"""

	queries['Average/Max/Min Gropee Gropes by Class'] = """
	SELECT class, SUM(grope_count), COUNT(grope_count), AVG(grope_count), MIN(grope_count), MAX(grope_count)
	    FROM gropee_grope_counts GROUP BY class ORDER BY class;
	"""

	return queries


def generate_HTML_table(query_results, border = 1, table_class='class_table', th_class='class_th',
                        tr_odd_class='class_tr', tr_even_class='class_tr', maps=None):
    if maps is None:
        maps = {}

    cols = query_results['cols']

    L = ["<TABLE BORDER={0} CLASS='{1}'>\n".format(border, table_class)]
    # TH
    L.append("\t<TR>")
    for col_name in cols:
        L.append("<TH CLASS='{0}'>".format(th_class))
        L.append(str(col_name))
        L.append("</TH>")
    L.append("</TR>\n\n")
    
    # TD
    row_num = 0
    for row in query_results['data']:
        row_num += 1
        L.append("\t<TR CLASS='{0}'>".format(tr_odd_class if (row_num % 2 == 1) else tr_even_class))
        col_idx = 0
        for s in row:
            L.append("<TD>")
            L.append(str(s) if cols[col_idx] not in maps else maps[cols[col_idx]](s))
            L.append("</TD>")
            col_idx += 1
        L.append("</TR>\n")

    L.append("</TABLE>\n")

    return ''.join(L)


def get_user(ip, cursor, trim = False):
    d = None
    try:
        cursor.execute("SELECT * FROM players where ip=%s", (ip,))
        cols = [cn[0] for cn in cursor.description]
        for row in cursor:
            this_row = [s.strip() if hasattr(s, 'strip') else s for s in row] if trim else row
            d = dict(zip(cols, this_row))
    except psycopg2.DatabaseError, e:
        d = None

    return d


def get_user_at(x_pos, y_pos, cursor, trim = False):
    d = None
    try:
        cursor.execute("SELECT * FROM players where location_x=%s AND location_y=%s", (x_pos, y_pos))
        cols = [cn[0] for cn in cursor.description]
        for row in cursor:
            this_row = [s.strip() if hasattr(s, 'strip') else s for s in row] if trim else row
            d = dict(zip(cols, this_row))
            break
    except psycopg2.DatabaseError, e:
        d = None
        
    return d


def move_user_to(ip, x_pos, y_pos, cursor):
    cursor.execute("UPDATE players SET location_x=%s, location_y=%s WHERE ip=%s", (x_pos, y_pos, ip))
    return cursor.rowcount


# def add_message(ip, message, intval1 = 0, intval2 = 0, intval3 = 0, intval4 = 0, strval = ""):
#     ret_code = 0
#     conn = None
#     try:
#         conn = db_connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO messages VALUES (%s,%s,%s,%s,%s,%s,%s)", (ip, message, intval1, intval2, intval3, intval4, strval))
#         conn.commit()
#         ret_code = cursor.rowcount
#     except psycopg2.DatabaseError, e:
#         if conn:
#             conn.rollback()
#         ret_code = -1
#     finally:
#         if conn:
#             conn.close()
#     return ret_code


def add_message(ip, message, intval1 = 0, intval2 = 0, intval3 = 0, intval4 = 0, strval = "", cursor = None):
    conn = None
    connect_here = False
    if cursor is None:
        connect_here = True
    if connect_here:
        conn = db_connection()
        cursor = conn.cursor()

    cursor.execute("INSERT INTO messages VALUES (%s,%s,%s,%s,%s,%s,%s)", (ip, message, intval1, intval2, intval3, intval4, strval))
    ret_code = cursor.rowcount

    if connect_here:
        conn.commit()
        conn.close()

    return ret_code


def pull_messages(ip):
    results = []
    conn = None
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION; LOCK TABLE players IN ACCESS EXCLUSIVE MODE;")

        results = query_results_to_list_of_dicts(get_query_results("SELECT * FROM messages WHERE ip=\'{0}\'".format(ip)))
        cursor.execute("DELETE FROM messages WHERE ip=%s", (ip,))

        cursor.execute("COMMIT;")
        #conn.commit()
           
    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        return []
        
    finally:
        
        if conn:
            conn.close()
        return results


def get_move_count(ip, cursor):
    count = 0
    cursor.execute("SELECT moves from players WHERE ip=%s", (ip,))
    for r in cursor:
        count = r[0]
    return count

def get_burn_count(ip, cursor):
    count = 0
    cursor.execute("SELECT burns from players WHERE ip=%s", (ip,))
    for r in cursor:
        count = r[0]
    return count


def get_grope_count_insert_if_not_present(ip1, ip2, cursor):
    cursor.execute("SELECT EXISTS (SELECT 1 from gropes WHERE groper=%s AND gropee=%s)", (ip1, ip2))
    found = False
    for r in cursor:
        found = r[0]
        
    count = 0
    if found:
        cursor.execute("SELECT count from gropes WHERE groper=%s AND gropee=%s", (ip1, ip2))
        for r in cursor:
            count = r[0]
    else:
        cursor.execute("INSERT INTO gropes (groper,gropee) SELECT %s, %s WHERE NOT EXISTS (SELECT groper, gropee from gropes WHERE groper=%s AND gropee=%s)",
                       (ip1, ip2, ip1, ip2))
    return count

def increment_grope_record(ip1, ip2, cursor):
    current_count = get_grope_count_insert_if_not_present(ip1, ip2, cursor)
    cursor.execute("UPDATE gropes SET count=%s WHERE groper=%s AND gropee=%s", (current_count+1, ip1, ip2))
    return current_count+1

def increment_move_record(ip, cursor):
    current_count = get_move_count(ip, cursor)
    cursor.execute("UPDATE players SET moves=%s WHERE ip=%s", (current_count+1, ip))
    return current_count+1

def increment_burn_record(ip, cursor):
    current_count = get_burn_count(ip, cursor)
    cursor.execute("UPDATE players SET burns=%s WHERE ip=%s", (current_count+1, ip))
    return current_count+1

def attempt_move_to(ip, x_move, y_move):
    conn = None
    d = {'user_found': False, 'free_move': False}
    try:
        conn = psycopg2.connect(host='localhost', port=5432, database='BumpyMaps', user='BumpyMaps', password='BumpBumpBump')
        
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION; LOCK TABLE players IN ACCESS EXCLUSIVE MODE;")
        
        this_user = get_user(ip, cursor)
        if this_user is not None:
            d['user_found'] = True

        if d['user_found']:
            user_at_other_location = get_user_at(this_user['location_x']+x_move, this_user['location_y']+y_move, cursor)
            if user_at_other_location is None:
                d['free_move'] = True
            else:
                d['free_move'] = False

            if d['free_move']:
                # Unemcumbered Move
                move_user_to(ip, this_user['location_x']+x_move, this_user['location_y']+y_move, cursor)
                increment_move_record(ip, cursor)
                # step sound message
                # inform of new position by message
                add_message(ip, game_messages["moved"], cursor = cursor)
            else:
                # Collision
                # grunts on both sides
                add_message(ip, game_messages["collide"], cursor = cursor)
                add_message(user_at_other_location['ip'], game_messages["collided into"], cursor = cursor)
                increment_grope_record(ip, user_at_other_location['ip'], cursor)
        
        cursor.execute("COMMIT;")
        get_query_results("SELECT * FROM players where ip=\'{0}\'".format(ip))
        #conn.commit()
           
    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        d = {'user_found': False, 'free_move': False, 'msg': []}
        
    finally:
        
        if conn:
            conn.close()
        d['msg'] = pull_messages(ip)
        return d
