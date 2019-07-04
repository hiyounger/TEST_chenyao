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
@app.route('/member/<condition>' , methods=['GET'])
def get_members_by_tel(condition=None):
    if request.method == 'GET':
        if condition.startswith('tel_'):
            tel = condition.split('_')[-1]
            ret_dic = Member.search_by_tel(tel)
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'Get Member by tel success'
            return jsonify(ret_dic)
        else:
            uid = int(condition.split('_')[-1])
            ret_dic = Member.serch_member_by_uid(uid)
            if len(ret_dic) == 0:
                ret_dic['return_code'] = 400
                ret_dic['return_msg'] = 'Get Member by uid faild'
            else:
                ret_dic['return_code'] = 200
                ret_dic['return_msg'] = 'Get Member by uid success'
            return jsonify(ret_dic)

# 查找大于给定积分的用户--闫振兴
@app.route('/filter/score')
def get_members_byScore():
    score = request.args['le']
    ret_dict = Member.get_member_byScore(score)
    ret_dict['return_code'] = 200
    ret_dict['return_msg'] = "Filter user success"
    print (ret_dict)
    return jsonify(ret_dict)



#根据用户金额更改用户积分  杨俊
@app.route('/member/<condition>' , methods=['PATCH'])
def surpermark_member(condition=None):
    if condition != None:
        if request.method == 'PATCH':
            uid = int(condition.split("_")[-1])
            score = int(request.form['score'])
            ret_dic = Member.update_member_score(uid, score)
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'update score success'
            return jsonify(ret_dic)


# 根据uid修改用户信息
@app.route('/member/<condition>' , methods=['PUT'])
def member_uid(condition=None):
    if condition != None:
        if request.method == 'PUT':
            user_info={}
            uid = int(condition.split("_")[-1])
            tel=request.form['tel']
            discount=request.form['discount']
            score= request.form['score']
            active=request.form['active']
            user_info={
                'tel':tel,
                'discount':discount,
                'score':score,
                'active':active
            }
            ret_dic = Member.update_msg_by_uid(uid, user_info)
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'update update member by uid success'
            return jsonify(ret_dic)


# 根据UID注销
@app.route('/member/<condition>', methods=['DELETE'])
def delete_member(condition=None):
    if request.method == 'DELETE':
        uid = int(condition.split("_")[-1])
        ret_dic = Member.delete_member(uid)
        if len(ret_dic) == 0:
            ret_dic['return_code'] = 400
            ret_dic['return_msg'] = 'Delete user failed'
        else:
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'Delete user success'
        print(ret_dic)
        return jsonify(ret_dic)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
