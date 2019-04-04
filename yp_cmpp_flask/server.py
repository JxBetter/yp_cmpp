import time
import pymysql
from src.cmpp import Cmpp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def connect_db(host, port, user, pwd, db_name):
    connect = pymysql.Connect(
        host=host,
        port=port,
        user=user,
        passwd=pwd,
        db=db_name,
        charset='utf8'
    )
    cursor = connect.cursor()
    return connect, cursor


conn, cur = connect_db('119.23.216.161', 3306, 'guest', 'helloworld', 'yp_cmpp_database')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)

    un = request.form.get('username')
    pwd = request.form.get('password')
    mobile = request.form.get('mobile')
    content = request.form.get('content')

    c = Cmpp('118.178.110.140', '30001', un, pwd, '0')
    f1 = c.connect_server()
    if f1 is False:
        sql = 'INSERT INTO cmpp_log (ip, 用户名, 密码, 手机号, 短信内容, 发送时间, 发送状态) VALUE ("{}", "{}", "{}", "{}", "{}", "{}")'.format(
            request.remote_addr, un, pwd, mobile, content, strTime, '失败')
        cur.execute(sql)
        conn.commit()
        return jsonify({'result': '连接cmpp服务器失败'})
    f2, conn_data = c.connect_application()
    if f2 is False:
        sql = 'INSERT INTO cmpp_log (ip, 用户名, 密码, 手机号, 短信内容, 发送时间, 发送状态) VALUE ("{}", "{}", "{}", "{}", "{}", "{}")'.format(
            request.remote_addr, un, pwd, mobile, content, strTime, '失败')
        cur.execute(sql)
        conn.commit()
        return jsonify({'result': '登陆cmpp失败，状态码为{}'.format(conn_data)})
    f3, send_data = c.send_message([mobile], content)
    if f3 is False:
        sql = 'INSERT INTO cmpp_log (ip, 用户名, 密码, 手机号, 短信内容, 发送时间, 发送状态) VALUE ("{}", "{}", "{}", "{}", "{}", "{}")'.format(
            request.remote_addr, un, pwd, mobile, content, strTime, '失败')
        cur.execute(sql)
        conn.commit()
        return jsonify({'result': '发送短信失败，状态码为{}'.format(send_data)})
    sql = 'INSERT INTO cmpp_log (ip, 用户名, 密码, 手机号, 短信内容, 发送时间, 发送状态) VALUE ("{}", "{}", "{}", "{}", "{}", "{}")'.format(
        request.remote_addr, un,pwd,mobile,content,strTime,'成功')
    cur.execute(sql)
    conn.commit()
    return jsonify({'result': 'ok'})


if __name__ == '__main__':
    app.run(port=5000)
