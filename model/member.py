#encoding:utf-8
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
class Member(db.Model):
    uid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tel=db.Column(db.String(11),unique=True,nullable=False)
    discount = db.Column(db.FLOAT,nullable=False,default=1)
    score = db.Column(db.Integer,nullable=False,default=0)
    active = db.Column(db.Integer,nullable=False,default=1)

    __tablename__ = 'members'

    # 根据手机号码注册新用户--童一鉴
    @classmethod
    def add_member_by_tel(cls, tel):
        member = Member()
        member.tel = tel
        db.session.add(member)
        db.session.commit()
        ret_dic = cls.search_by_tel(tel)['members'][0]
        return ret_dic
    @classmethod
    def add_memebr(cls, tel):
        member = Member()
        member.tel = tel
        db.session.add(member)
        db.session.commit()
        ret_dic = cls.search_by_tel(tel)['members'][0]
        return ret_dic


    @classmethod
    def serch_by_tel(cls, tel):
        member_list = []
        if len(tel) == 11:
            member = Member.query.filter(Member.tel.endswith(tel))
            member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.disc, 'score': member.score,
                           'active': member.active}
            member_list.append(member_info)
        else:
            db_query = Member.query.filter(Member.tel.endwith(tel))
            for member in db_query:
                member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.disc, 'score': member.score,
                               'active': member.active}
                member_list.append(member_info)
                ret_dic = {
                    'new_member': member_info,
                    'count': len(member_list),
                    'members': member_list
                }
        return ret_dic

    __tablename__='members'
    # 获取积分大于指定值的会员列表

    # 根据手机号码注册新用户--童一鉴
    @classmethod
    def add_member_by_tel(cls, tel):
        member = Member()
        member.tel = tel
        db.session.add(member)
        db.session.commit()
        ret_dic = cls.search_by_tel(tel)['members'][0]
        return ret_dic

    @classmethod
    def serch_by_tel(cls, tel):
        member_list = []
        if len(tel) == 11:
            member = Member.query.filter(Member.tel.endswith(tel))
            member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.disc, 'score': member.score,
                           'active': member.active}
            member_list.append(member_info)
        else:
            db_query = Member.query.filter(Member.tel.endwith(tel))
            for member in db_query:
                member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.disc, 'score': member.score,
                               'active': member.active}
                member_list.append(member_info)
                ret_dic = {
                    'new_member': member_info,
                    'count': len(member_list),
                    'members': member_list
                }
        return ret_dic

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

    @classmethod  # 根据手机号查询会员信息
    def search_by_tel(cls, tel):
        member_list = []
        if len(tel) == 11:  # 当号码为11位时
            member = Member.query.filter(Member.tel == tel).first()
            member_info = {"uid": member.uid, "tel": member.tel, "discount": member.discount,
                           "score": member.score, "active": member.active}
            member_list.append(member_info)
        else:  # 输入尾号位数查询会员信息
            db_query = Member.query.filter(Member.tel.endswith(tel))
            for member in db_query:
                member_info = {"uid": member.uid, "tel": member.tel, "discount": member.discount,
                               "score": member.score, "active": member.active}
                member_list.append(member_info)

        ret_dic = {
            "count": len(member_list),
            "members": member_list
        }
        return ret_dic

    @classmethod
    def delete_member(cls, uid):
        for i in range(len(Member.members)):
            if Member.members[i]['uid'] == uid:
                Member.members[i]['state'] ='0'
                Member.members[i]['discount'] = '1'
                ret_dic = {
                    'uid': Member.members[i]['uid'],
                    'tel': Member.members[i]['tel'],
                    'state': '0',
                    'discount': Member.members[i]['discount']
                }
                return ret_dic
            else:
                ret_dic={
                    'ret_code':400,
                    'ret_msg':'Delete,fail'
                }
            return ret_dic

    # 根据实付金额更改用户积分
    @classmethod
    def update_member_score(cls, uid, score):
        member = Member.query.filter(Member.uid == uid).first()
        score_before = member.score
        member.score = score_before + score
        db.session.commit()

        ret_dic = {"uid": member.uid, 'tel': member.tel, 'score_before': score_before, 'score_after': member.score,
                   'score_change': score}
        return ret_dic
