# __encoding:utf-8__

from flask import Flask, request, jsonify
from WYF.member import Member

app = Flask('__main__')


@app.route('/jsontest')
def json_test():
    ret_dic = {
        'return_code': 200,
        'msg': 'get member list success',
        'members': [
            {'id': 1, 'tel': '18812345671', 'discount': 0.98, 'state': 1, 'jifen': 1000},
            {'id': 2, 'tel': '18812345672', 'discount': 0.9, 'state': 1, 'jifen': 1500},
            {'id': 3, 'tel': '18812345673', 'discount': 0.8, 'state': 1, 'jifen': 2000},
            {'id': 4, 'tel': '18832145673', 'discount': 0.8, 'state': 1, 'jifen': 2000}
        ]
    }
    return jsonify(ret_dic)


@app.route('/member')
@app.route('/member/<condition>', methods=['GET', 'DELETE'])
def members_info(condition=None):
    if request.method == 'GET':
        if condition == None:
            members_list = Member.get_all_members()
            members_list['return_code'] = 200
            members_list['return_msg'] = 'Get member list success'
            return jsonify(members_list)
    elif request.method == 'DELETE':
        uid = condition.split('_')[-1]
        ret_dic = Member.delete_member(uid)
        ret_dic['return_code'] = 200
        ret_dic['return_msg'] = 'Update user success'
        return jsonify(ret_dic)
    else:
        ret_dic = {'return_code': 200, 'return_msg': '什么都没做'}
        return jsonify(ret_dic)


if __name__ == '__main__':
    app.run()
