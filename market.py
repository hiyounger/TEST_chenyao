# encoding:utf-8
from flask import Flask, jsonify, request
from model.member import db, Member

app = Flask(__name__)
# 配置数据库连接
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/supermarket"
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


# 根据手机号添加会员  ---童一鉴
@app.route('/member', methods=['POST'])
def member_actions(condition=None):
    # 1.处理创建
    if request.method == 'GET':
        if condition == None:
            member_list = Member.get_all_members()
            member_list['return_code'] = 200
            member_list['return_msg'] = '获取用户成功'
    elif request.method == 'POST':
        tel = request.form['tel']
        mem_info = Member.add_member_by_tel(tel)
        ret_dic = {
            "return_code": 200, "return_msg": "add member success",
            "member": mem_info
        }
        return jsonify(ret_dic)


# 根据手机号码查找会员列表  ---liu
@app.route('/mermber/<condition>' , methods=['GET'])
def get_members_by_tel(condition=None):
    if request.method == 'GET':
        if condition.startswith('tel_'):
            tel = condition.split('_')[-1]
            ret_dic = Member.search_by_tel(tel)
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'Get Member by tel success'
            return jsonify(ret_dic)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
