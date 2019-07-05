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
def member_actions():
    tel = request.form['tel']
    if len(tel) == 11:  # 判断tel长度是否等于11
        result = request.form['tel'].isdigit()  # result是tel转换成数字，判断是否为真
        if result == True:  # 如果为真, 即长度为11位，类型为整数
            tel = request.form['tel']
            mem_info = Member.add_member_by_tel(tel)
            ret_dic = {
                "return_code": 200, "return_msg": "add member success",
                "member": mem_info
            }
            return jsonify(ret_dic)
        elif tel in Member.search_by_tel:  # 如果手机号已存在   and ret_dic_act == 1 :
            ret_dic = {
                "return_code": 508, "return_msg": "add member failed, exists",
            }
            return jsonify(ret_dic)
        else:  # and ret_dic_act == 1 :
            # tel = request.form['tel']
            ret_dic = {
                "return_code": 508, "return_msg": "add member failed, exists",
            }
            return jsonify(ret_dic)
    else:
        ret_dic = {
            "return_code": 508, "return_msg": "add member failed, exists",
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


#根据uid修改用户信息  陈耀
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
        uid = condition.split("_")[-1]
        result=uid.isdigit()
        ret_dic = Member.delete_member(uid)
        if result==True:
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'Delete user success'
            return jsonify(ret_dic)

        else:
            ret_dic['return_code'] = 400
            ret_dic['return_msg'] = 'Delete user faild'
            return jsonify(ret_dic)

@app.route('/member')
def get_all_mermbers_list():
    ret_dict=Member.get_all_members()
    return jsonify(ret_dict)



if __name__ == '__main__':
    app.run( port=5000, debug=True)
