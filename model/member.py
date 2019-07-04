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

    # @classmethod
    # def add_member(cls,tel):
    #     mem = Member()
    #     mem.tel = tel
    #     db.session.add(mem)
    #     db.session.commit()
    #     ret_dic = {
    #                "mem": {"uid": mem.uid, "tel": mem.tel, "discount": mem.discount,
    #                        "score": mem.score, "active": mem.active}
    #                }
    #     return ret_dic

    @classmethod
    def delete_member(cls, uid):
        results = Member.query.filter(Member.uid==uid)[0]
        db.session.delete(results)
        db.session.commit()
        # for i in range(len(Member.members)):
        #     if str(Member.members[i]['uid']) == uid:
        #         Member.members[i]['state'] ='0'
        #         Member.members[i]['discount'] = '1'
        #         ret_dic = {
        #             'uid': Member.members[i]['uid'],
        #             'tel': Member.members[i]['tel'],
        #             'state': '0',
        #             'discount': Member.members[i]['discount']
        #         }
        ret_dic={"uid": results.uid, 'tel': results.tel, 'discount': results, 'score': results.score,
                   'active': results.active}
        return ret_dic




