
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Healthcare_api.views import DoctorViewSet, PatientViewSet, MappingListCreateView, MappingDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'api/doctors', DoctorViewSet, basename='doctor')
router.register(r'api/patients', PatientViewSet, basename='patient')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/mappings/', MappingListCreateView.as_view(), name='mappings_root'),
    path('api/mappings/<int:id>/', MappingDetailView.as_view(), name='mapping_by_id'),
]
