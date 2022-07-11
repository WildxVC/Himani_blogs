from django.urls import path
from . import views
# from . views import AddPost
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    # path('adminLogin', views.adminLogin, name="adminLogin"),
    # path('login', views.admin_login, name="login"),
    # path('logout', views.logoutView, name="logout"),
    path('addPost',views.addPost, name="addPost"),
    path('search', views.searchResult, name="searchResult"),
    path('about', views.aboutView, name="about"),
    path('terms', views.termsView, name="terms"),
    path('privacy', views.privacyView, name="privacy"),
    path('category/<slug:category_slug>', views.categories, name="categories"),
    path('<slug:slug>', views.viewPost, name="viewPost"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)