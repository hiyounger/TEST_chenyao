#encoding:utf-8
from YZX.db import memberDB
class memModel():
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
