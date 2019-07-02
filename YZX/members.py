#encoding:utf-8
from flask import Flask ,request ,jsonify
from YZX.model.memberModel import memModel

app=Flask('__main__')
@app.route('/')
def hello ():
    return 'hello'
@app.route('/members',methods=['GET','POST'])
@app.route('/members/<condition>',methods=['GET','PATCH','PUT','DELETE'])
def get_members_way(condition=None):
    if request.method=='GET':
        if condition==None:
            ret_dict=memModel.get_all_members_stateNotZero()
            return jsonify(ret_dict)






if __name__ == '__main__':
    app.run()