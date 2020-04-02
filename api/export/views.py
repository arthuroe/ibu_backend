
import logging

from flask import make_response, jsonify
from flask.views import MethodView
import flask_excel as excel

from api.models import Patient, Treatment, Drug
from api.models import db


class ExportFailureException(Exception):
    """
    Failed file export.
    """
    pass


class ExportView(MethodView):
    """
    View to export information
    """
    def get(self):
        try:
            return excel.make_response_from_tables(db.session, [Patient, Treatment, Drug], "xls")
        except ExportFailureException as e:
            logging.error("File export failed: {}".format(e))
            response = {
                'status': 'fail',
                'message': 'An error has occurred. Please try again.'
            }
            return make_response(jsonify(response)), 500
