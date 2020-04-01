from api.models import db, ModelMixin


class Drug(ModelMixin):
    """
    Drug model attributes
    """
    __tablename__ = 'drugs'

    name = db.Column(db.String(180))
