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


#根据手机号查找会员列表  ---liu
@classmethod
def search_by_tel(cls, tel):
    member_list = []
    if len(tel) == 11:
        member = Member.query.filter(Member.tel.endswith(tel))
        member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.disc, 'score': member.score,
                       'active': member.active}
        member_list.append(member_info)
    else:
        db_query = Member.query.filter(Member.tel.endwith(tel))
        for member in db_query:
            member_info = {'uid': member.uid, 'tel': member.tel, 'discount': member.discount, 'score': member.score,
                           'active': member.active}
            member_list.append(member_info)
            ret_dic = {
                'new_member': member_info,
                'count': len(member_list),
                'members': member_list
            }
    return ret_dic
