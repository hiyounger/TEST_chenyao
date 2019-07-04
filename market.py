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
@app.route('/initdb',methods=['POST'])
def init_db():
    db.create_all()
    ret_dic={
        'return_code':200,
        'return_msg':'Init db success'
    }
    return jsonify(ret_dic)

@app.route('/member<condition>',methods=['DELETD'])
def delete_member(condition=None):
    # if request.method=='POST':
    #     tel=request.form['tel']
    #     mem_info=Member.add_member(tel)
    #     ret_dic={
    #         "ret_code": "200",
    #         "ret_msg": "添加会员信息成功",
    #         'member':mem_info
    #     }
    #     return jsonify(ret_dic)
    if request.method == 'DELETE':
        uid = request.form['uid']
        ret_dic = Member.delete_member(uid)
        ret_dic['return_code'] = 200
        ret_dic['return_msg'] = 'Delete user success'
        return jsonify(ret_dic)


# @app.route('/all_member')
# def all_member(tel):
#     db_query = Member.query.all()
#     member_list = []
#     for mem in db_query:
#         mem_info = {'uid': mem.uid, 'tel': mem.tel, 'discount': mem.discount, 'score': mem.score,'active':mem.active}
#         member_list.append(mem_info)
#
#     ret_dic = {'ret_code': '200', 'ret_msg': '查询信息成功',
#                'member': member_list, 'count': len(member_list)}
#     return jsonify(ret_dic)





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)