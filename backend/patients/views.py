from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Patient

class PatientView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        age = request.data.get('age')
        condition = request.data.get('condition')

        if not all([name, age, condition]):
            return Response({'error': 'name, age, and condition are required'}, status=400)

        try:
            patient = Patient.objects.create(
                created_by=request.user,
                name=name,
                age=age,
                condition=condition
            )
            return Response({
                'id': str(patient.id),
                'created_by': patient.created_by.id,
                'name': patient.name,
                'age': patient.age,
                'condition': patient.condition
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def get(self, request, id=None):
        try:
            if id is not None:
                try:
                    patient = Patient.objects.get(id=id, created_by=request.user)
                except Patient.DoesNotExist:
                    return Response({'error': 'Patient not found'}, status=404)

                return Response({
                    'id': str(patient.id),
                    'created_by': patient.created_by.id,
                    'name': patient.name,
                    'age': patient.age,
                    'condition': patient.condition,
                    'doctor_id': str(patient.doctor.id) if patient.doctor else None
                }, status=status.HTTP_200_OK)
            else:
                patients = Patient.objects.filter(created_by=request.user)
                data = [{
                    'id': str(p.id),
                    'created_by': p.created_by.id,
                    'name': p.name,
                    'age': p.age,
                    'condition': p.condition,
                    'doctor_id': str(p.doctor.id) if p.doctor else None
                } for p in patients]
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Patient ID is required'}, status=400)

        try:
            try:
                patient = Patient.objects.get(id=id, created_by=request.user)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient not found or unauthorized'}, status=404)

            updated = False
            for field in ['name', 'age', 'condition']:
                if field in request.data:
                    setattr(patient, field, request.data.get(field))
                    updated = True

            if updated:
                patient.save()

            return Response({
                'id': str(patient.id),
                'created_by': patient.created_by.id,
                'name': patient.name,
                'age': patient.age,
                'condition': patient.condition,
                'doctor_id': str(patient.doctor.id) if patient.doctor else None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'Patient ID is required'}, status=400)

        try:
            try:
                patient = Patient.objects.get(id=id, created_by=request.user)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient not found or unauthorized'}, status=404)

            patient.delete()
            return Response({'message': 'Patient deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
