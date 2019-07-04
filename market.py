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
    return 'Hello Flask'
@app.route('/initdb',methods=['POST'])
def init_db():
    db.create_all()
    ret_dic={
        'return_code':200,
        'return_msg':'Init db success'
    }
    return jsonify(ret_dic)


@app.route('/members/<condition>',methods=['GET','POST','PUT','PATCH','DELETE'])
def member_actions(condition=None):
    if request.method =='GET':
        if condition.startswith('tel'):
            tel = condition.split('_')[-1]
            ret_dic =Member.serch_by_tel(tel)
            ret_dic['return_code'] = 200
            ret_dic['return_msg'] = 'Get Member by tel success'
            return jsonify(ret_dic)
    # elif request.method =='POST':
    #     tel = request.form['tel']
    #     mem_info = Member.add_memebr(tel)
    #
    #     ret_dic = {
    #         'return_code':200,
    #         'return_msg':'add member success',
    #         'member':mem_info
    #     }
    #     return jsonify(ret_dic)
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80,debug=True)