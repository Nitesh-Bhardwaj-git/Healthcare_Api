from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor, PatientDoctorMapping, Patient
from .serializers import DoctorSerializer, PatientDoctorMappingSerializer, PatientSerializer


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by('id')
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('id')
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MappingListCreateView(APIView):
    def get(self, request):
        mappings = PatientDoctorMapping.objects.select_related('patient', 'doctor').all()
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(PatientDoctorMappingSerializer(mapping).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MappingDetailView(APIView):
    def get(self, request, id: int):
        mappings = PatientDoctorMapping.objects.select_related('doctor').filter(patient_id=id)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def delete(self, request, id: int):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            mapping = PatientDoctorMapping.objects.get(pk=id)
        except PatientDoctorMapping.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

