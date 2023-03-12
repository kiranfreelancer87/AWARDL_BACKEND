import json
import time
import logging
import flask
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'awardl'

log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

mysql = MySQL(app)


@app.route('/postResult', methods=['POST'])
def postResult():
    if flask.request.json is not None and flask.request.method == "POST":
        cur = mysql.connection.cursor()
        reqBody = flask.request.json
        cur.execute(
            "INSERT INTO `gamehistory` (`id`, `name`, `email`, `seconds`, `guesses`, `points`) VALUES (NULL, %s, %s, %s, %s, %s)",
            (reqBody['name'], reqBody['email'], reqBody['seconds'], reqBody['numberOfGuesses'], reqBody['score']))
        mysql.connection.commit()
        cur.close()
        return json.dumps(flask.request.json)
    else:
        return json.dumps({'message': "Invalid Request"})


@app.route('/getWords', methods=['GET'])
def getWords():
    wordList = []
    for w in list(open('words.csv', 'r').read().split('\n')):
        if len(w) == 5:
            wordList.append(w)
    return json.dumps({"data": wordList})


@app.route('/getLeaderboard', methods=['GET'])
def getLeaderboard():
    if flask.request.method == "GET":

        res = []

        counter = 1

        lastUpdatedPoint = 0

        try:

            cur = mysql.connection.cursor()
            cur.execute("SELECT DISTINCT email FROM gamehistory")
            idArr = []
            for tmpEmail in cur.fetchall():
                cur.execute(
                    "SELECT id from gamehistory where email = '{0}' ORDER by points DESC LIMIT 1".format(tmpEmail[0]))
                idArr.append(cur.fetchone()[0])
            if len(idArr) == 0:
                res = []
                for i in range(10 - len(res)):
                    res.append({'id': 'na', 'name': 'na', 'time': 'na', 'guesses': 'na', 'points': 'na'})
                return res
            idInStr = str(idArr).replace("[", "").replace("]", "").replace(" ", "")
            cur.execute(
                "WITH cte AS (SELECT *,DENSE_RANK() OVER(ORDER BY points DESC, seconds ASC) AS rank FROM gamehistory g where id IN (" + idInStr + ")) SELECT * FROM cte ORDER BY rank ASC, points DESC, seconds ASC, name ASC limit 10")
            dbRes = cur.fetchall()

            if res is not None and len(dbRes) > 0:
                for r in dbRes:
                    if str(r[5]).endswith(".0") or str(r[5]).endswith(".00"):
                        pts = str(int(str(r[5]).replace(".0", "").replace(".00", "")))
                    else:
                        pts = str(r[5])

                    res.append({'id': str(r[6]),
                                'name': str(str(r[1]).split(" ")[0]).capitalize() + " " + str(str(r[1]).split(" ")[1])[
                                    0].capitalize() + ".", 'time': time.strftime('%M:%S', time.gmtime(int(r[3]))),
                                'guesses': str(r[4]) + ' guesses', 'points': pts})

                    if lastUpdatedPoint is not r[5]:
                        counter = counter + 1

                    lastUpdatedPoint = r[5]

            cur.close()

        except Exception as e:
            res = {"message": e}

        if res is None:
            res = []

        if len(res) < 10:
            for i in range(10 - len(res)):
                res.append({'id': 'na', 'name': 'na', 'time': 'na', 'guesses': 'na', 'points': 'na'})
        resp = flask.Response(json.dumps({"data": res}))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        return json.dumps({"message": "Invalid Request"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
