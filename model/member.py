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
        type= tel.isdigit()
        if len(tel) == 11 and type == True :
            member = Member.query.filter(Member.tel.endswith(tel)).first()
            member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.discount, 'score': member.score,
                           'active': member.active}
            member_list.append(member_info)
        elif len(tel) == 4 and type == True:
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



    # 根据实付金额更改用户积分杨俊
    @classmethod
    def update_member_score(cls, uid, score):
        member = Member.query.filter(Member.uid == uid).first()
        if member == None:
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
        else:
            ret_dic = {
                "count": len(member_list),
                "members": member_list
            }
        return ret_dic
        # 方法二：从数据库中查找到积分大于给定积分的用户，遍历增添进member_list中
        # members = Member.query.filter(Member.score >=int(sc))
        # for mem in members:
        #     member_list.append(mem)
        # ret_dic={
        #  "count":len(member_list),
        #  "members":member_list
        # }
        # return ret_dic


    #根据uid，修改用户信息    ---陈耀
    @classmethod
    def update_msg_by_uid(cls, uid,user_info):
        member_list = []
        member = Member.query.filter(Member.uid == uid).first()
        member_info = {"uid": int(member.uid), "tel": user_info['tel'], "discount": user_info['discount'],
                       "score": user_info['score'], "active": user_info['active']}
        member_list.append(member_info)
        db.session.commit()
        ret_dic = {
            "members": member_list
        }
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
