import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView


from api.decorators import token_required
from api.models import Patient


class PatientView(MethodView):
    """
    View to manage patients
    """
    decorators = [token_required]

    def get(self, current_user, patient_id=None):
        try:
            if patient_id:
                patient = Patient.find_first(id=patient_id)
                if not patient:
                    response = {
                        'status': 'fail',
                        'message': 'Patient does not exist'
                    }
                    return make_response(jsonify(response)), 400

                response = {
                    'status': 'success',
                    'patient': patient.serialize()
                }
                return make_response(jsonify(response)), 200

            patients = Patient.fetch_all()

            if not patients:
                response = {
                    'status': 'success',
                    'message': 'No patients have been added'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'success',
                'patients': [patient.serialize() for patient in patients]
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to retrieve patients.'
            }
            return make_response(jsonify(response)), 500

    def post(self, current_user):
        kwargs = request.json
        phone_number = kwargs.get('phone_number')

        if not phone_number:
            response = {
                'status': 'fail',
                'message': 'Phone number is required.'
            }
            return make_response(jsonify(response)), 400

        patient = Patient.find_first(phone_number=kwargs.get('phone_number'))
        kp_code = (
            kwargs.get('first_name')[0] + kwargs.get('second_name')[0] +
            kwargs.get('third_name')[0] + str(
                int(kwargs.get('date_of_birth')[5:7])) +
            str(int(kwargs.get('date_of_birth')[0:4])) + kwargs.get('gender')[0]
        )
        kwargs.update({"kp_code": kp_code})
        if not patient:
            try:
                patient = Patient(**kwargs)
                patient.save()

                response = {
                    'status': 'success',
                    'message': f"Successfully Added {kwargs.get('first_name')}."
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                logging.error(f"An error has occurred  {e}")
                response = {
                    'status': 'fail',
                    'message': 'Failed to add patient. Please try again.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'Patient already exists.',
            }
            return make_response(jsonify(response)), 409

    def put(self, current_user, patient_id):
        kwargs = request.json
        kwargs.update({"id": patient_id})

        try:
            patient = Patient.find_first(id=patient_id)
            if patient:
                patient.update(**kwargs)

                response = {
                    'status': 'success',
                    'message': f'Successfully updated {patient.first_name}.'
                }
                return make_response(jsonify(response)), 201

            response = {
                'status': 'fail',
                'message': 'Patient does not exist.',
            }
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Update failed. Please try again.'
            }
            return make_response(jsonify(response)), 500

    def delete(self, current_user, patient_id):
        try:
            patient = Patient.find_first(id=patient_id)
            if patient:
                patient.delete()
                response = {
                    'status': 'success',
                    'message': f'Successfully deleted {patient.first_name}.'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'fail',
                'message': 'Patient does not exist.',
            }
            return make_response(jsonify(response)), 400

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Delete failed. Please try again.'
            }
            return make_response(jsonify(response)), 500
