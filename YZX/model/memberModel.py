#encoding:utf-8
from YZX.db import memberDB
class memModel():
    # 返会没有注销的所有用户
    @classmethod
    def get_all_members_stateNotZero(cls):
        member_list=[]
        for mem in memberDB.members:
            if mem['state']!=0:
                member_list.append(mem)
        ret_dic={
            'members':member_list
        }
        return ret_dic
#     根据手机号码返回用户列表
    @classmethod
    def get_member_byTel(cls,tel):
        member_list=[]
        if len(tel)==11 or len(tel)==4 :
            for mem in memberDB.members:
                if mem['tel']==tel:
                    member_list.append(mem)
                if mem['tel'].endswith(tel):
                    member_list.append(mem)
            if len(member_list)==0:
                member_list=['您输入的手机号码或手机号码后四位不存在']
            ret_dic={
                     'count':len(member_list),
                     'members':member_list
                 }
            return ret_dic
        else:
            ret_dic = {
                'count': len(member_list),
                'members': 'Get Member by tel false(输入tel错误)'
            }
            return ret_dic
#     根据id查询用户列表
    @classmethod
    def get_member_byUID(cls,uid):
        member_list=[]
        for mem in memberDB.members:
            if mem['id']==uid:
                member_list.append(mem)
                ret_dic={
                    'members':member_list
                }
                return ret_dic
        ret_dic = {
            'members': '请输入存在的用户uid或者正确uid'
        }
        return ret_dic

    # 根据手机号码增加用户
    @classmethod
    def add_member_byTel(cls,tel):
        member_list=[]
        #判断tel是否符合规范
        if len(tel)==11:
            #  判断用户是否存在
            for mem in memberDB.members:
                if mem['tel']==tel:
                    #  再判断state是否为0
                    if mem['state']==0:
                         # 注销的用户，需要我们将它重新更新为使用状态
                        mem['state']==1
                        member_list.append(mem)
                        ret_dic={
                            'return_code':200,
                            'return_msg':'add member success',
                            'members':member_list
                        }
                        return ret_dic
                    else:
                        ret_dic = {
                            'return_code': 508,
                            'return_msg': 'add member failed, exists',
                        }
                        return ret_dic
                else:
                    memberDB.members.append({'id': str(len(memberDB.members)+1), 'tel': tel, 'disc': 1.0, 'state': 1, 'points': 0000})
                    member_list = [
                        {'id': str(len(memberDB.members)), 'tel': tel, 'disc': 1.0, 'state': 1, 'points': 0000}
                    ]
                    ret_dic={
                        'return_code': 200,
                        'return_msg': 'add member success',
                        'members':member_list
                    }
                    return ret_dic
        else:
            ret_dic = {
                'return_code': 508,
                'return_msg': 'add member failed, exists',
            }
            return ret_dic

    #更新用户信息
    @classmethod
    def update_member(cls,uid,new_info_dic):
        for i in range(len(memberDB.members)):
            if memberDB.members[i]['id'] == uid:
                for key in new_info_dic.keys():
                    memberDB.members[i][key] = new_info_dic[key]
                return memberDB.members[i]
        return {}







