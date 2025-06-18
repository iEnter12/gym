class Facility(db.Model):
    __tablename__ = 'facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, default=1)  # 1: 可用, 0: 维护中, 2: 已关闭
    image_url = db.Column(db.String(500))
    min_booking_duration = db.Column(db.Integer, default=1)
    max_booking_duration = db.Column(db.Integer, default=4)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 