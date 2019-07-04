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

    @classmethod
    def delete_member(cls, uid):
        mem = Member.query.all()
        if mem.uid==uid:
            db.session.delete(mem)
            db.session.commit()
        ret_dic = {"uid": mem.uid, 'tel': mem.tel, 'discount': mem.discount, 'score': mem.score,
                   'active': mem.active}
        return ret_dic





