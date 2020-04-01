from datetime import datetime

from api.models import db, ModelMixin


class Patient(ModelMixin):
    """
    Patient model attributes
    """
    __tablename__ = 'patients'

    first_name = db.Column(db.String(180))
    second_name = db.Column(db.String(180))
    third_name = db.Column(db.String(180))
    kp_code = db.Column(db.String(180))
    gender = db.Column(db.String(180))
    date_of_birth = db.Column(db.DateTime)
    kp_hotspot_site = db.Column(db.String(180))
    phone_number = db.Column(db.String(180))
    employed = db.Column(db.Boolean, default=False)
    occupation = db.Column(db.String(180))
    relationship_status = db.Column(db.String(180))
    education_level = db.Column(db.String(180))
    treatments = db.relationship('Treatment', backref='patient', lazy='dynamic')
