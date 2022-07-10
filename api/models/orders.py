from ..utils import db
from enum import Enum
from datetime import datetime

class Size(Enum):
    SMALL='small'
    MEDIUM='medium'
    LARGE='Large'
    EXTRA_LARGE='extra_large'

class OrderStatus(Enum):
    PENDING= 'pending'
    IN_TRANSIT='in-transit'
    DELIVERED='delivered'

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer(), primary_key=True)
    size=db.Column(db.Enum(Size),default=Size.SMALL)
    order_status=db.Column(db.Enum(OrderStatus),default=OrderStatus.PENDING)
    flavour=db.Column(db.String(),nullable=False)
    quantity=db.Column(db.Integer())
    date_created=db.Column(db.DateTime(),default=datetime.utcnow)
    user=db.Column(db.Integer(),db.ForeignKey('users.id'))

    def __str__(self):
        return f'<Order {self.id}>'


    def save(self):
        db.session(self)
        db.session()



    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)



    def delete(self):
        db.session.delete(self)
        db.session.commit()