from customer.views import CustomerRegisterAPIView
from loan.views import CheckEligibilityView, CreateLoanView, ViewLoanView, ViewLoansView
from django.contrib import admin
from django.urls import path, include
from config.views import DataInsertView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Credit Approval System API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/insert/", DataInsertView.as_view()),
    path("api/v1/register/", CustomerRegisterAPIView.as_view()),
    path("api/v1/check-eligibility/", CheckEligibilityView.as_view()),
    path("api/v1/create-loan/", CreateLoanView.as_view()),
    path("api/v1/view-loan/<int:loan_id>/", ViewLoanView.as_view()),
    path("api/v1/view-loans/<int:customer_id>", ViewLoansView.as_view()),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
