from django.urls import path, include

urlpatterns = [
    path('api/', include('authentication.urls')),
    path('api/', include('authorization.urls')),
    path('api/', include('mock_business.urls')),
]
