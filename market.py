# encoding:utf-8
from flask import Flask, jsonify, request
from model.member import db, Member
import config

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://%s:%s@%s:%s/%s" % (
                                config.DB_USERNAME, config.DB_PASSWORD, config.DB_HOST, config.DB_PORT, config.DB_NAME)
db.init_app(app)


@app.route('/')
def index():
    return 'Hellow Flask'


@app.route('/initdb', methods=['POST'])
def init_db():
    db.create_all()
    ret_dic = {
        'return_code': 200,
        'return_msg': 'Init db success'
    }
    return jsonify(ret_dic)


@app.route('/member', methods=['POST'])
def member_actions(condition=None):
    # 1.处理创建
    if request.method == 'POST':
        tel = request.form['tel']
        mem_info = Member.add_member_by_tel(tel)
        ret_dic = {
            "return_code": 200, "return_msg": "add member success",
            "member": mem_info
        }
        return jsonify(ret_dic)


@app.route('/member/uid', methods=['DELETD'])
def delete_member():
    if request.method == 'DELETE':
        uid = request.form['uid']
        ret_dic = Member.delete_member(uid)
        ret_dic['return_code'] = 200
        ret_dic['return_msg'] = 'Delete user success'
        print(ret_dic)
        return jsonify(ret_dic)


if __name__ == '__main__':
    app.run(host=config.APP_HOST, port=config.APP_PORT)
    # app.run(host='0.0.0.0', port=5001)
