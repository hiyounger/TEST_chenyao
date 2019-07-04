#encoding:utf-8
from flask import Flask,jsonify,request
from model.member import db,Member
app=Flask(__name__)
#配置数据库连接
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/supermarket"
db.init_app(app)
@app.route('/')
def index():
    return 'Hellow Flask'

@app.route("/member", methods=['GET', 'POST'])
@app.route('/member/<condition>', methods=['GET', 'PUT','PATCH'])
def get_all_members(condition=None):
    if request.method == 'GET':
        if condition == None:
            member_list = Member.get_all_members()
            member_list['return_code'] = 200
            member_list['return_msg'] = '获取用户成功'
@app.route('/initdb',methods=['POST'])
def init_db():
    db.create_all()
    ret_dic={
        'return_code':200,
        'return_msg':'Init db success'
    }
    return jsonify(ret_dic)

@app.route('/member/uid',methods=['DELETD'])
def delete_member():
    if request.method == 'DELETE':
        uid = request.form['uid']
        ret_dic = Member.delete_member(uid)
        ret_dic['return_code'] = 200
        ret_dic['return_msg'] = 'Delete user success'
        print(ret_dic)
        return jsonify(ret_dic)




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)