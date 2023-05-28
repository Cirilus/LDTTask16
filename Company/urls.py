from django.urls import path, include
from rest_framework import routers
from .views import CompanyViews, ProjectViews, \
    AdminVacanciesViews, AddCurator, \
    CompanyVacanciesView, SubscribeOnVacancyView, \
    DetailVacancyViews, DetailCompanyViews, UserVacanciesViews, StatisticViews

router = routers.DefaultRouter()
router.register('company', DetailCompanyViews, basename="detail_company")
router.register('companies', CompanyViews, basename="companies")


router.register('project', ProjectViews, basename="projects")

router.register('admin/vacancies', AdminVacanciesViews, basename="admin_vacancy")
router.register('vacancies', UserVacanciesViews, basename="user_vacancy")
router.register('vacancies', DetailVacancyViews, basename="detail_project")

router.register("statistic", StatisticViews, basename="statistic")


urlpatterns = [
    path("", include(router.urls)),
    path("company/<int:id>/add/", AddCurator.as_view({"post": "post", "delete": "delete"}), name="Add Curator"),
    path("company/myvacancies/", CompanyVacanciesView.as_view({"get": "get"}), name="Company vacancies"),
    path("vacancy/subscribe/<int:id>", SubscribeOnVacancyView.as_view({"get": "get"}), name="Subscribe on vacancies"),
]
