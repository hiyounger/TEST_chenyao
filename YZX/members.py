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
        else:
            if condition.startswith('tel_'):
                tel = condition.split('_')[-1]
                ret_dict=memModel.get_member_byTel(tel)
                ret_dict['return_code']=200
                ret_dict['return_msg']='Get Member by tel success'
                return jsonify(ret_dict)
            elif condition.startswith('uid_'):
                uid=condition.split('_')[-1]
                ret_dict=memModel.get_member_byUID(uid)
                return jsonify(ret_dict)
            else:
                ret_dict={
                    'members':'请输入tel_或者uid_ ,非tel_，uid_查询不出用户'
                }
                return jsonify(ret_dict)
    elif request.method == 'POST':
        tel=request.form['tel']
        ret_dict=memModel.add_member_byTel(str(tel))
        return jsonify(ret_dict)
    elif request.method == "PUT":
        uid = condition.split('_')[-1]
        disc = request.form['disc']
        tel = request.form['tel']
        state = request.form['state']
        user_info = {'disc': disc, 'tel': tel, 'state': state}
        update_member = memModel.update_member_by_id(uid, user_info)
        if len(update_member) == 0:
            update_member['return_code'] = 404
            update_member['return_msg'] = "update member by id false"
        else:
            update_member['return_code'] = 202
            update_member['return_msg'] = "update member by id sucessful"
        return jsonify(update_member)











if __name__ == '__main__':
    app.run()