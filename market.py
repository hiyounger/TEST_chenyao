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




# 根据手机号码注册用户
@app.route('/member', methods=['POST'])
@app.route('/member/<condition>', methods=['GET', 'PUT','PATCH'])
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

    if condition == None:
        if request.method == 'PATCH':
            uid = int(condition.split("_")[-1])
            score = int(request.form['score'])
            ret_dic = Member.update_member_score(uid, score)
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'update score success'
            return jsonify(ret_dic)

        # 写http：//127.0.0.1/members下的程序
        pass
    else:
        if request.method == 'GET':
            pass
        elif request.method == '请求方法':
            pass


# 查找大于给定积分的用户
@app.route('/filter/score')
def get_members_byScore():
    score = request.args['le']
    ret_dict = Member.get_member_byScore(score)
    ret_dict['return_code'] = 200
    ret_dict['return_msg'] = "Filter user success"
    print (ret_dict)
    return jsonify(ret_dict)


# 根据手机号码注册用户
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

# 根据id删除用户
@app.route('/member/uid', methods=['DELETD'])
def delete_member(uid):
    if request.method == 'DELETE':
        mem_uid = request.form['uid']
        mem= Member.query.filter(Member.uid==mem_uid)[0]
        db.session.delete(mem)
        db.session.commit()
        ret_dic = Member.delete_member(uid)
        ret_dic['return_code'] = 200
        ret_dic['return_msg'] = 'Delete user success'
        print(ret_dic)
        return jsonify(ret_dic)


# 根据手机号码查找用户列表

@app.route('/mermber/<condition>' , methods=['GET'])
def get_members_by_tel(condition=None):
    if request.method == 'GET':
        if condition.startswith('tel_'):
            tel = condition.split('_')[-1]
            ret_dic = Member.serch_by_tel(tel)
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'Get Member by tel success'
            return jsonify(ret_dic)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
