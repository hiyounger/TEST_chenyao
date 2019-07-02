# __encoding:utf-8__
from WYF import mysql
class Member():
    @classmethod
    def get_all_members(cls):
        member_dic = {
            'members': mysql.members
        }
        return member_dic
    @classmethod
    def delete_member(cls, uid):
        for i in range(len(mysql.members)):
            if str(mysql.members[i]['uid']) == uid:
                mysql.members[i]['state'] = '0'
                mysql.members[i]['discount'] = '1'
                ret_dic = {
                    'uid': mysql.members[i]['uid'],
                    'tel': mysql.members[i]['tel'],
                    'state': '0',
                    'discount': mysql.members[i]['discount']
                }
                return ret_dic
