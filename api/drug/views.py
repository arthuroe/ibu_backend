import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView


from api.decorators import token_required
from api.models import Drug


class DrugView(MethodView):
    """
    View to manage drugs
    """
    decorators = [token_required]

    def get(self, current_user, drug_id=None):
        try:
            if drug_id:
                drug = Drug.find_first(id=drug_id)
                if not drug:
                    response = {
                        'status': 'fail',
                        'message': 'Drug does not exist'
                    }
                    return make_response(jsonify(response)), 400

                response = {
                    'status': 'success',
                    'drug': drug.serialize()
                }
                return make_response(jsonify(response)), 200

            drugs = Drug.fetch_all()

            if not drugs:
                response = {
                    'status': 'success',
                    'message': 'No drugs have been added'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'success',
                'drugs': [drug.serialize() for drug in drugs]
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to retrieve drugs.'
            }
            return make_response(jsonify(response)), 500

    def post(self, current_user):
        kwargs = request.json

        try:
            drug = Drug(**kwargs)
            drug.save()

            response = {
                'status': 'success',
                'message': f'Successfully Added {drug.name}.'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add drug. Please try again.'
            }
            return make_response(jsonify(response)), 500

    def put(self, current_user, drug_id):
        kwargs = request.json
        kwargs.update({"id": drug_id})

        try:
            drug = Drug.find_first(id=drug_id)
            if drug:
                drug.update(**kwargs)

                response = {
                    'status': 'success',
                    'message': f'Successfully updated {drug.name}.'
                }
                return make_response(jsonify(response)), 201

            response = {
                'status': 'fail',
                'message': 'Drug does not exist.',
            }
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Update failed. Please try again.'
            }
            return make_response(jsonify(response)), 500

    def delete(self, current_user, drug_id):
        try:
            drug = Drug.find_first(id=drug_id)
            if drug:
                drug.delete()
                response = {
                    'status': 'success',
                    'message': f'Successfully deleted {drug.name}.'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'fail',
                'message': 'Drug does not exist.',
            }
            return make_response(jsonify(response)), 400

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Delete failed. Please try again.'
            }
            return make_response(jsonify(response)), 500
