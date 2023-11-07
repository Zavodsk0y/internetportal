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
                  path('applications/create', ApplicationCreateView.as_view(), name='app-create'),
                  path('applications/<int:pk>/delete', ApplicationDeleteView.as_view(), name='app-delete'),
                  path('admin/', AdminView.as_view(), name='admin'),
                  path('applications/<int:pk>/update', AdminUpdateApplicationView.as_view(), name='app-update'),
                  path('categories/<int:pk>/delete', AdminDeleteCategoryView.as_view(), name='category-delete'),
                  path('categories/create', AdminCreateCategoryView.as_view(), name='category-create'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
