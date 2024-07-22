"""
URL configuration for intro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from Apphome.views import checkout, home,detail, category_list_view, insertComs, vendor_list_view, search_view
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # r = rowstring 
    # path(r vide, nom_anle_page_ho_sokafana)
    path(r'',home,name="home"),
    path(r'detail/<int:x>',detail,name="detail"),
    path(r'insertcoms',insertComs,name="commenter"),

    path(r'checkout/',checkout,name="checkout"),
    path(r'category/<cid>',category_list_view,name="category_list"),
    path(r'vendor/',vendor_list_view,name="vendor_list"),
    path(r'search/',search_view,name="search_list"),    
    path("",include("AppInscription.urls")),
    path("",include("AppPanier.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
