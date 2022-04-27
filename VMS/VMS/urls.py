"""VMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from VMS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('admin-login/', views.adminLogin),
    path('admin-login/dashboard/', views.adminDashboard),
    path('admin-login/dashboard/add-student/', views.addStudent),
    path('admin-login/dashboard/student-details/', views.studentDetails),
    path('admin-login/dashboard/student-details/details/<student_id>', views.studentFullDetail),
    path('admin-login/dashboard/student-details/edit/<student_id>', views.studentEditDetails),
    path('admin-login/dashboard/add-vendor/', views.adminAddVendor),
    path('admin-login/dashboard/edit-vendor/<vid>', views.adminEditVendor),
    path('admin-login/dashboard/delete-vendor/<vid>', views.adminDeleteVendor),
    path('admin-login/dashboard/vendor-details/', views.adminVendorDetails),
    path('admin-login/dashboard/vendor-view-details/<vid>', views.adminVendorViewDetails),
    path('admin-login/logout/', views.adminLogout),

    path('student-login/', views.studentLogin),
    path('student-login/dashboard/', views.studentDashboard),
    path('student-login/dashboard/outlet/<outlet_name>', views.studentOutlet),
    path('student-login/dashboard/expense/', views.studentExpense),
    path('student-login/dashboard/current-orders/', views.studentCurrentOrders),
    path('student-login/dashboard/past-orders/', views.studentPastOrders),
    path('student-login/dashboard/past-orders/details/', views.studentPastOrderDetails),
    path('student-login/dashboard/outlet/cart/<vendor_name>', views.studentCart),
    path('student-login/dashboard/outlet/cart/order-complete/', views.orderComplete, name='order-complete'),
    path('logout/', views.logout),
    
    path('vendor-login/', views.vendorLogin),
    path('vendor-login/dashboard/', views.vendorDashboard),
    path('vendor-login/dashboard/shop-status/<int:status>', views.vendorDashboard),
    path('vendor-login/dashboard/edit-item/<item_id>', views.vendorEditItem),
    path('vendor-login/dashboard/delete-item/<item_id>', views.vendorDeleteItem),
    path('vendor-login/dashboard/add-item/', views.vendorAddItem),
    path('vendor-login/dashboard/current-orders/', views.vendorCurrentOrders),
    path('vendor-login/dashboard/current-orders/prepared/<oid>', views.vendorCurrentOrdersPrepared),
    path('vendor-login/dashboard/past-orders/', views.vendorPastOrders),
    path('vendor-login/dashboard/past-orders/details/<oid>', views.vendorPastOrderDetails),
    path('vendor-login/dashboard/income/', views.vendorIncome),
    path('vendor-login/logout/', views.vendorLogout),

    # path('form/', views.tempUserform),
]
