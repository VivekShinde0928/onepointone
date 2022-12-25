from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('home', views.home),
    path('',views.login_access,name='login'),
    path('logout',views.logout,name='logout'),
    path('login_data',views.login,name='login_data'),
    path('onepointone', views.csv_page,name='csv_page'),
    path('upload_csv', views.upload_csv,name='upload_csv'),
    path('empForm', views.empForm,name='empForm'),
    path('addEmp', views.addEmp,name='addEmp'),
    path('editEmp/<int:id>', views.editEmp, name="editEmp"),
    path('saveEditEmp', views.saveEditEmp, name="saveEditEmp"),
    path('deleteEmp/<int:id>', views.deleteEmp, name="deleteEmp"),
    path('downloadCSV', views.downloadCSV, name="downloadCSV"),
]