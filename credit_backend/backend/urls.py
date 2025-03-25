from django.contrib import admin
from django.urls import path, include
from backend import views  # ✅ Import authentication views directly

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Authentication routes
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('auth/google/', views.GoogleAuthView.as_view(), name='google-auth'),

    path('api/user/me/', views.get_user_profile, name='user-profile'),


    # ✅ Finance Tracker URLs under /finance_tracker/
    path('finance_tracker/', include('backend.finance_tracker.urls')),  
]
