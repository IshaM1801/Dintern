from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from patients.models import Patient
from doctors.models import Doctor

class MappingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        patient_id = request.data.get('patient_id')
        doctor_id = request.data.get('doctor_id')

        if not all([patient_id, doctor_id]):
            return Response({'error': 'patient_id and doctor_id are required'}, status=400)

        try:
            try:
                patient = Patient.objects.get(id=patient_id, created_by=request.user)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient not found or unauthorized'}, status=404)

            try:
                doctor = Doctor.objects.get(id=doctor_id)
            except Doctor.DoesNotExist:
                return Response({'error': 'Doctor not found'}, status=404)

            patient.doctor = doctor
            patient.save()

            return Response({
                'message': 'Doctor successfully assigned to patient',
                'patient': {
                    'id': str(patient.id),
                    'name': patient.name,
                    'doctor_id': str(patient.doctor.id)
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def get(self, request, patient_id=None):
        try:
            if patient_id is not None:
                try:
                    patient = Patient.objects.get(id=patient_id)
                except Patient.DoesNotExist:
                    return Response({'error': 'Patient not found'}, status=404)

                if not patient.doctor:
                    return Response({'error': 'No doctor assigned to this patient'}, status=404)

                doctor = patient.doctor
                return Response({
                    'id': str(doctor.id),
                    'created_by': doctor.created_by.id,
                    'name': doctor.name,
                    'specialty': doctor.specialty,
                    'experience': doctor.experience
                }, status=status.HTTP_200_OK)
            else:
                # Select all patients who have an assigned doctor (doctor is not null)
                patients = Patient.objects.filter(doctor__isnull=False)
                mappings = [{
                    'patient_name': p.name,
                    'doctor_name': p.doctor.name
                } for p in patients]

                return Response(mappings, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def delete(self, request, patient_id=None):
        if patient_id is None:
            return Response({'error': 'Patient ID is required'}, status=400)

        try:
            try:
                patient = Patient.objects.get(id=patient_id, created_by=request.user)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient not found or unauthorized'}, status=404)

            patient.doctor = None
            patient.save()

            return Response({'message': 'Doctor successfully removed from patient'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
