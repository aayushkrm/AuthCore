from django.urls import path
from .views import (
    AccessRulesListCreateView, 
    AccessRuleDetailView,
    RolesListView,
    BusinessElementsListView
)

urlpatterns = [
    path('access-rules/', AccessRulesListCreateView.as_view(), name='access-rules-list'),
    path('access-rules/<int:pk>/', AccessRuleDetailView.as_view(), name='access-rule-detail'),
    path('roles/', RolesListView.as_view(), name='roles-list'),
    path('business-elements/', BusinessElementsListView.as_view(), name='business-elements-list'),
]
