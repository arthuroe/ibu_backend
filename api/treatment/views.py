import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView


from api.decorators import token_required
from api.models import Treatment, Drug


class TreatmentView(MethodView):
    """
    View to manage patient treatments
    """
    decorators = [token_required]

    def get(self, current_user, patient_id=None, treatment_id=None):
        try:
            if treatment_id:
                treatment = Treatment.find_first(id=treatment_id)
                if not treatment:
                    response = {
                        'status': 'fail',
                        'message': 'Treatment does not exist'
                    }
                    return make_response(jsonify(response)), 400

                response = {
                    'status': 'success',
                    'treatment': treatment.serialize()
                }
                return make_response(jsonify(response)), 200

            treatments = Treatment.filter_by(patient_id=patient_id)

            if not treatments:
                response = {
                    'status': 'success',
                    'message': 'No treatments have been added'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'success',
                'treatments': [treatment.serialize() for treatment in treatments]
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to retrieve treatments.'
            }
            return make_response(jsonify(response)), 500

    def post(self, current_user, patient_id=None):
        kwargs = request.json
        kwargs.update({"patient_id": patient_id})
        print(kwargs)
        try:
            treatment = Treatment(**kwargs)
            treatment.save()

            response = {
                'status': 'success',
                'message': f'Successfully Added treatment.'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add treatment. Please try again.'
            }
            return make_response(jsonify(response)), 500

    def put(self, current_user, treatment_id):
        kwargs = request.json
        kwargs.update({"id": treatment_id})

        try:
            treatment = Treatment.find_first(id=treatment_id)
            if treatment:
                treatment.update(**kwargs)

                response = {
                    'status': 'success',
                    'message': f'Successfully updated treatment.'
                }
                return make_response(jsonify(response)), 201

            response = {
                'status': 'fail',
                'message': 'Treatment does not exist.',
            }
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Update failed. Please try again.'
            }
            return make_response(jsonify(response)), 500

    def delete(self, current_user, treatment_id):
        try:
            treatment = Treatment.find_first(id=treatment_id)
            if treatment:
                treatment.delete()
                response = {
                    'status': 'success',
                    'message': f'Successfully deleted treatment'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'fail',
                'message': 'Treatment does not exist.',
            }
            return make_response(jsonify(response)), 400

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Delete failed. Please try again.'
            }
            return make_response(jsonify(response)), 500


class TreatmentDrugView(MethodView):
    """
    View to manage treatments and drugs
    """
    decorators = [token_required]

    def post(self, current_user, treatment_id):
        kwargs = request.json

        try:
            drug = Drug.find_first(id=kwargs.get('drug_id'))
            if not drug:
                response = {
                    'status': 'fail',
                    'message': 'Drug does not exist'
                }
                return make_response(jsonify(response)), 400

            treatment = Treatment.find_first(id=treatment_id)
            treatment.drugs.append(drug)
            treatment.save()

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
