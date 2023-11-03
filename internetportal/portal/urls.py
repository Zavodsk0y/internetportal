from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
                  path('', Index.as_view(), name='index'),
                  path('signup/', RegisterUserView.as_view(), name='registration'),
                  path('login/', LoginUserView.as_view(), name='login'),
                  path('logout/', LogoutUserView.as_view(), name='logout'),
                  path('profile/', UserProfileView.as_view(), name='profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
