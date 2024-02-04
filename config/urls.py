from customer.views import CustomerRegisterAPIView
from loan.views import CheckEligibilityView, CreateLoanView, ViewLoanView, ViewLoansView
from django.contrib import admin
from django.urls import path, include
from config.views import DataInsertView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/insert/", DataInsertView.as_view()),
    path("api/v1/register/", CustomerRegisterAPIView.as_view()),
    path("api/v1/check-eligibility/", CheckEligibilityView.as_view()),
    path("api/v1/create-loan/", CreateLoanView.as_view()),
    path("api/v1/view-loan/<int:loan_id>/", ViewLoanView.as_view()),
    path("api/v1/view-loans/<int:customer_id>", ViewLoansView.as_view()),
]
