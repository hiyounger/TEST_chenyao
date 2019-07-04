#encoding:utf-8
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
class Member(db.Model):
    uid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tel=db.Column(db.String(11),unique=True,nullable=False)
    discount = db.Column(db.FLOAT,nullable=False,default=1)
    score = db.Column(db.Integer,nullable=False,default=0)
    active = db.Column(db.Integer,nullable=False,default=1)

    __tablename__='members'

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
        mem = Member.query.all()
        if mem.uid==uid:
            db.session.delete(mem)
            db.session.commit()
        ret_dic = {"uid": mem.uid, 'tel': mem.tel, 'discount': mem.discount, 'score': mem.score,
                   'active': mem.active}
        return ret_dic





