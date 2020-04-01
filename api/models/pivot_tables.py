from api.models import db

db.Table('treatment_drugs',
         db.Column('treatment_id', db.Integer,
                   db.ForeignKey('treatments.id')),
         db.Column('drug_id', db.Integer, db.ForeignKey('drugs.id'))
         )
