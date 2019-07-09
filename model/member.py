# encoding:utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Member(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tel = db.Column(db.String(11), unique=True, nullable=False)
    discount = db.Column(db.FLOAT, nullable=False, default=1)
    score = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Integer, nullable=False, default=1)

    __tablename__ = 'members'

    # 根据手机号添加会员  ---童一鉴
    @classmethod  # 添加会员
    def add_member_by_tel(cls, tel):
        member = Member()
        member.tel = tel
        db.session.add(member)
        db.session.commit()
        ret_dic = cls.search_by_tel(tel)['members'][0]
        return ret_dic



    # 根据手机号查找会员列表  ---liu
    @classmethod
    def search_by_tel(cls, tel):
        member_list = []
        type = tel.isdigit()
        member = Member.query.filter(Member.tel.endswith(tel)).first()
        if len(tel) == 11 and type == True and member != None:
            member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.discount, 'score': member.score,
                           'active': member.active}
            member_list.append(member_info)
            ret_dic = {
                'count': len(member_list),
                'members': member_list
            }
            return ret_dic
        elif len(tel) == 4 and type == True and member != None:
            db_query = Member.query.filter(Member.tel.endswith(tel))
            for member in db_query:
                member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.discount, 'score': member.score,
                               'active': member.active}
                member_list.append(member_info)
                ret_dic = {
                    'count': len(member_list),
                    'members': member_list
                }
                return ret_dic
        else:
            ret_dic={
                'return_code':400,
                'return_msg':'Get Member by tel failed'
            }
            return ret_dic


    # 根据实付金额更改用户积分杨俊
    @classmethod
    def update_member_score(cls, uid, score):
        member = Member.query.filter(Member.uid == uid).first()
        if member==None:
            ret_dic = {}
            return ret_dic

        score_before = member.score
        member.score = score_before + score
        db.session.commit()

        ret_dic = {"uid": member.uid, 'tel': member.tel, 'score_before': score_before, 'score_after': member.score,
                       'score_change': score}
        return ret_dic


    # 通过uid查询会员信息(zhangjun)
    @classmethod
    def serch_member_by_uid(cls, uid):
        ret_query = Member.query.all()
        for member in ret_query:
            if member.uid == uid:
                ret_dic = {
                    'uid': member.uid,
                    'tel': member.tel,
                    'discount': member.discount,
                    'score': member.score,
                    'active':member.active,
                }
                return ret_dic
        return {}

    # 获取积分大于指定值的会员列表--闫振兴
    @classmethod
    def get_member_byScore(cls, score):
        member_list = []
        # 判断传入的le是否为int类型
        # 若score是字母，特殊字符的时候，返回输入正确的值
        # 若score是小数，将score加一在判断。
        try:
            sc = int(score)
            if sc < float(score):
                sc += 1
        except:
            member_list = ['请输入正确的数值']
            ret_dic = {
                'return_code':400,
                'members': member_list
            }
            return ret_dic
        # 方法一：从数据库中查找所有用户，
        # 逐个遍历，找到积分大于给定积分的用户，增添进member_list中
        members = Member.query.all()
        for mem in members:
            if mem.score >= sc:
                member_info = {"uid": mem.uid, 'tel': mem.tel, 'discount': mem.discount, 'score': mem.score,
                               'active': mem.active}
                member_list.append(member_info)
        if len(member_list) == 0:
            ret_dic = {
                "count": 0,
                "members": member_list
            }
            ret_dic['return_code'] = 200
        else:
            ret_dic = {
                "count": len(member_list),
                "members": member_list
            }
            ret_dic['return_code'] = 200
        return ret_dic
        # 方法二：从数据库中查找到积分大于给定积分的用户，遍历增添进member_list中
        #
        # members = Member.query.filter(Member.score >=int(sc))
        # for mem in members:
        #     member_list.append(mem)
        # ret_dic={
        #  "count":len(member_list),
        #  "members":member_list
        # }
        # return ret_dic


    #根据uid，修改用户信息   陈耀
    @classmethod
    def update_member_by_uid(cls, uid, member, new_tel, new_discount, new_score, new_active):
        if uid == "" or new_tel == "" or new_discount == "" or new_score == "" or new_active == "":
            ret_dic = {"return_code": "400",
                       "return_msg": "修改的值不能为空"}
            return ret_dic
        elif new_active != "0" and new_active != "1":
            ret_dic = {"return_code": "400",
                       "return_msg": "激活状态只能为0或1"}
            return ret_dic
        elif float(new_discount) < 0 and float(new_discount) > 1:
            ret_dic = {"renturn_code": "400",
                       "return_msg": "会员折扣应该在0~1之间"
                       }
            return ret_dic
        elif int(new_score) < 0:
            ret_dic = {"return_code": "400",
                       "return_msg": "积分不能为负数"}
            return ret_dic
        elif len(new_tel) != 11:
            ret_dic = {"return_code": "400",
                       "return_msg": "电话号码应该为11位数字"}
            return ret_dic

        try:
            new_tel = int(new_tel)
        except:
            ret_dic = {"return_code": "400",
                       "return_msg": "电话号码应该为数字"}
            return ret_dic

        member.tel = str(new_tel)
        member.active = int(new_active)
        member.discount = float(new_discount)
        member.score = int(new_score)
        try:
            db.session.commit()
        except:
            ret_dic = {"return_code": "400",
                       "return_msg": "手机号是唯一的，您输入的手机号数据库的列表中已存在"}
            return ret_dic
        ret_dic = {"uid": member.uid, 'tel': member.tel, 'discount': member.discount,
                   'score': member.score, 'active': member.active}
        return ret_dic


    # 根据uid注销
    @classmethod
    def delete_member(cls, uid):
        ret_query = Member.query.all()
        for member in ret_query:
            if member.uid == uid:
                member.active = 0
                member.discount = 1
                ret_dic = {
                    'uid': member.uid,
                    'tel': member.tel,
                    'active': member.active,
                    'discount': member.discount
                }
                return ret_dic
        return {}

    #查询所有用户：
    @classmethod
    def get_all_members(cls):
        member_list=[]
        member=Member.query.all()
        for mem in member:
            member_info = {"uid": mem.uid, 'tel': mem.tel, 'discount': mem.discount, 'score': mem.score,
                               'active': mem.active}
            member_list.append(member_info)
        ret_dic={
            'members':member_list
        }
        return ret_dic
