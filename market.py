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
@app.route('/members',methods=['POST'])
@app.route('/members/<condition>',methods=['GET','PATCH'])
def surpermark_member(condition=None):
    if condition==None:
        # 写http：//127.0.0.1/members下的程序
        pass
    else:
        if request.method=='GET':
            pass
        elif request.method=='请求方法':
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)