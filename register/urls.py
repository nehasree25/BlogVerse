from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('createblog/',views.createBlog, name='createblog'),
    path('allblogs/',views.allBlogs,name='allblogs'),
    path('delete_blog/<int:id>/',views.delete_blog,name='delete_blog'),
    path('editblog/<int:id>', views.editblog, name='editblog'),
    path('myblogs/',views.myBlogs,name='myblogs'),
]
