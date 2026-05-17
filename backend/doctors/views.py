from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Doctor

class DoctorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        specialty = request.data.get('specialty')
        experience = request.data.get('experience')

        if not all([name, specialty, experience]):
            return Response({'error': 'name, specialty, and experience are required'}, status=400)

        try:
            doctor = Doctor.objects.create(
                created_by=request.user,
                name=name,
                specialty=specialty,
                experience=experience
            )
            return Response({
                'id': str(doctor.id),
                'created_by': doctor.created_by.id,
                'name': doctor.name,
                'specialty': doctor.specialty,
                'experience': doctor.experience
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def get(self, request, id=None):
        try:
            if id is not None:
                try:
                    doctor = Doctor.objects.get(id=id, created_by=request.user)
                except Doctor.DoesNotExist:
                    return Response({'error': 'Doctor not found'}, status=404)
                return Response({
                    'id': str(doctor.id),
                    'created_by': doctor.created_by.id,
                    'name': doctor.name,
                    'specialty': doctor.specialty,
                    'experience': doctor.experience
                }, status=status.HTTP_200_OK)
            else:
                doctors = Doctor.objects.filter(created_by=request.user)
                data = [{
                    'id': str(d.id),
                    'created_by': d.created_by.id,
                    'name': d.name,
                    'specialty': d.specialty,
                    'experience': d.experience
                } for d in doctors]
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Doctor ID is required'}, status=400)

        try:
            try:
                doctor = Doctor.objects.get(id=id, created_by=request.user)
            except Doctor.DoesNotExist:
                return Response({'error': 'Doctor not found or unauthorized'}, status=404)

            updated = False
            for field in ['name', 'specialty', 'experience']:
                if field in request.data:
                    setattr(doctor, field, request.data.get(field))
                    updated = True

            if updated:
                doctor.save()

            return Response({
                'id': str(doctor.id),
                'created_by': doctor.created_by.id,
                'name': doctor.name,
                'specialty': doctor.specialty,
                'experience': doctor.experience
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'Doctor ID is required'}, status=400)

        try:
            try:
                doctor = Doctor.objects.get(id=id, created_by=request.user)
            except Doctor.DoesNotExist:
                return Response({'error': 'Doctor not found or unauthorized'}, status=404)

            doctor.delete()
            return Response({'message': 'Doctor deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
