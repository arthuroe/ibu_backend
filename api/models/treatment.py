from datetime import datetime

from api.models import db, ModelMixin


class Treatment(ModelMixin):
    """
    Treatment model attributes
    """
    __tablename__ = 'treatments'

    reason = db.Column(db.String(180))
    category = db.Column(db.String(180))
    type_of_syndrome = db.Column(db.String(180))
    patient_id = db.Column(
        db.Integer, db.ForeignKey('patients.id'), nullable=False)
    new_client = db.Column(db.Boolean, default=False)
    bp = db.Column(db.String(180))
    weight = db.Column(db.String(180))
    refered_to_other_facility = db.Column(db.Boolean, default=False)
    facility_refered_to = db.Column(db.String(180))
    condom_given = db.Column(db.Boolean, default=False)
    lubricant_given = db.Column(db.Boolean, default=False)
    date_of_next_visit = db.Column(db.DateTime)
    comment = db.Column(db.String(180))
    drugs = db.relationship(
        'Drug', secondary='treatment_drugs', backref='treatments',
        lazy='dynamic'
    )
