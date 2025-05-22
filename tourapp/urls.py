from django.urls import path
from .import views as v


urlpatterns=[
    path('',v.index,name='index'),
    path('vreg/',v.vregis,name='vregis'),
    path('vlogin/',v.vlogin,name='vlogin'),
    path('logout/',v.vlogout,name='vlogout'),
    path('vdash/',v.vdashboard,name='vdashboard'),
    path('cpackage/',v.cpackages,name='cpack'),
    path('packagelist/',v.package_list,name='package_list'),
    path('epackages/<int:package_id>/',v.edit_packages,name='epack'),
    path('dpackages/<int:package_id>/',v.delete_package,name='delete_package'),
    path('edit-package/<int:package_id>/', v.edit_rejected_package, name='edit_package'),
    path('submit-draft/<int:package_id>/', v.submit_draft, name='submit_draft'),
    path('vbookings/', v.vendor_bookings, name='vendor_bookings'),
    path('terms/',v.terms,name='terms'),
    path('custreg/',v.userregister,name='uregis'),
    path('custlogin/',v.ulogin,name='ulogin'),
    path('clogout/',v.clogout,name='clogout'),
    path('custdash/',v.customer_dashboard,name='cdashboard'),
    path('package/<int:package_id>/', v.package_details, name='package_details'),
    path("book/<int:package_id>/", v.book_package, name="book_package"),
    path("confirm_payment/<int:booking_id>/", v.confirm_payment, name="confirm_payment"),
    path("cancel/<int:booking_id>/", v.cancel_booking, name="cancel_booking"),
    path('my-bookings/', v.booked_packages, name='booked_packages'),

]



