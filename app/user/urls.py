"""
    URLs Mapping for the User APIs
"""

from django.urls import path

from user import views

# Must be the same as the one in the test
app_name = 'user'


# create must be the same as the endpoint defined in the test
urlpatterns = [
    path('/create', views.CreateUserView.as_view(), name='create'),
    path('/token', views.CreateTokenView.as_view(), name='token'),
    path('/me', views.ManageUserView.as_view(), name='me')
]