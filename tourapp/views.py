from django.shortcuts import render,redirect,get_object_or_404
from .forms import VregistrationForm,VloginForm,PackageForm,CustregisterForm,CloginForm,BookingForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.http import HttpResponseForbidden
import razorpay



# Create your views here.
def index(request):
    # Fetching categorized packages
    top_packages = TourPackages.objects.filter(price__gte=50000,status__status='approved')  # High-price packages
    budget_packages =TourPackages.objects.filter(price__lte=25000,status__status='approved')  # Affordable packages
    destination_packages =TourPackages.objects.filter(status__status='approved')  # Show all destinations
    
    location_query = request.GET.get("location", None)  # Get location filter from user input
    if location_query:
        destination_packages = destination_packages.filter(location__icontains=location_query)

    return render(request, "index.html", {
        "top_packages": top_packages,
        "budget_packages": budget_packages,
        "destination_packages": destination_packages
    })


def vregis(request):
    if request.method=='POST':
        form=VregistrationForm(request.POST)
        if form.is_valid():
        
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=User.objects.create_user(username=username,password=password)
            Vendor.objects.create(user=user)
            return redirect('vlogin')
    else:
        form=VregistrationForm()
    return render(request,"vendorreg.html",{'form':form})  
 
def vlogin(request):
    if request.method=='POST':
        form=VloginForm(request,data=request.POST)
        if form.is_valid(): 
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('vdashboard')
            else:
                return render(request,"vendorlogin.html",{'form':form,'error':'invalid credentials'})
    else:
        form=VloginForm()
    return render(request,"vendorlogin.html",{'form':form})
       

def vlogout(request):
    logout(request)
    return redirect('index')

    

@login_required
def vdashboard(request):
    vendor=get_object_or_404(Vendor,user=request.user)
    packages=TourPackages.objects.filter(vendor=vendor)
    return render(request,"vendordashboard.html",{'packages':packages})

@login_required
def cpackages(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = vendor

            if 'save_draft' in request.POST:
                package.status = TourStatus.objects.get(status='draft')
                package.save()
                messages.success(request, "Saved as draft.")
                return redirect('vdashboard')

            elif 'submit_for_approval' in request.POST:
                # Validate availability range
                if not package.available_from or not package.available_to:
                    messages.error(request, "Both available from and to dates must be set.")
                    return render(request, "cpackage.html", {'form': form})

                if package.available_to < package.available_from:
                    messages.error(request, "Available to date cannot be earlier than available from date.")
                    return render(request, "cpackage.html", {'form': form})

                # Valid one-day package is allowed
                package.status = TourStatus.objects.get(status='pending approval')
                package.expiry_date = package.available_to
                package.save()
                messages.success(request, "Form submitted.")
                return redirect('vdashboard')

    else:
        form = PackageForm()

    return render(request, "cpackage.html", {'form': form})


@login_required
def edit_packages(request, package_id):
    package = get_object_or_404(TourPackages, id=package_id, vendor__user=request.user)
    form = PackageForm(request.POST or None,request.FILES ,instance=package)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('package_list')
    return render(request, 'epackage.html', {'form': form})

@login_required
def delete_package(request, package_id):
    package = get_object_or_404(TourPackages, id=package_id, vendor__user=request.user)
    package.delete()
    return redirect('package_list')

@login_required
def submit_draft(request, package_id):
    package = get_object_or_404(TourPackages, id=package_id, vendor__user=request.user)

    if package.status.status != "draft":
        messages.error(request, "Only draft packages can be submitted.")
        return redirect('package_list')  # or your vendor dashboard

    package.status = TourStatus.objects.get(status='pending approval')
    package.expiry_date = package.available_to  # ensure it's not null
    package.save()
    messages.success(request, "Package submitted for approval.")
    return redirect('package_list')


@login_required
def package_list(request):
    vendor = Vendor.objects.get(user=request.user)
    draft_packages = TourPackages.objects.filter(vendor=vendor, status__status='draft')
    submitted_packages = TourPackages.objects.filter(vendor=vendor, status__status='pending approval')
    approved_packages = TourPackages.objects.filter(vendor=vendor, status__status='approved')
    rejected_packages = TourPackages.objects.filter(vendor=vendor, status__status='rejected')
    
    context = {
        'draft_packages': draft_packages,
        'submitted_packages': submitted_packages,
        'approved_packages': approved_packages,
        'rejected_packages': rejected_packages,
    }
    return render(request, 'packages_list.html', context)

@login_required
def edit_rejected_package(request, package_id):
    package = get_object_or_404(TourPackages, id=package_id, vendor__user=request.user)
    if package.status.status != 'rejected':
        return HttpResponseForbidden("Only rejected packages can be edited.")

    if request.method == 'POST':
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            updated_package = form.save(commit=False)
            updated_package.status = TourStatus.objects.get(status='draft')  # Reset to draft
            updated_package.save()
            return redirect('vendor_packages')
    else:
        form = PackageForm(instance=package)

    return render(request, 'edit_package.html', {'form': form})

@login_required
def vendor_bookings(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    bookings = Booking.objects.filter(package__vendor=vendor).select_related('package', 'customer')

    return render(request, 'bookings.html', {'bookings': bookings})


def terms(request):
    return render(request,"terms of use.html")

def userregister(request):
    if request.method=='POST':
        form=CustregisterForm(request.POST)
        if form.is_valid():
        
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=User.objects.create_user(username=username,password=password)
            Customer.objects.create(user=user)
            return redirect('ulogin')
    else:
        form=CustregisterForm()
    return render(request,"customerreg.html",{'form':form})  
 

def ulogin(request):
    if request.method=='POST':
        form=CloginForm(request,data=request.POST)
        if form.is_valid(): 
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('cdashboard')
            else:
                return render(request,"user",{'form':form,'error':'invalid credentials'})
    else:
        form=CloginForm()
    return render(request,"customlogin.html",{'form':form})

def clogout(request):
    logout(request)
    return redirect('index')


def package_details(request, package_id):
    package = get_object_or_404(TourPackages, id=package_id)
    return render(request, 'package_details.html', {'package': package})

razorpay_client = razorpay.Client(auth=("rzp_test_RFCmnFJb7PAojP", "W8RNigEx15UMWVLljnBitoSA"))

@login_required
def customer_dashboard(request):
    packages = TourPackages.objects.filter(status__status="approved")
    return render(request, "custdashboard.html", {"packages": packages})

@login_required
def book_package(request, package_id):
    package = get_object_or_404(TourPackages, id=package_id)

    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.package = package
            booking.save()

            no_of_people=booking.no_of_people
            total_price=float(package.price)*no_of_people
            amount = int(total_price* 100)  

            payment = razorpay_client.order.create({
                "amount": amount,  # Ensure this is an integer
                "currency": "INR",
                "receipt": f"booking_{booking.id}",
                "payment_capture": 1
            })
        

            
            return render(request, "payment.html", {
    "booking": booking,
    "razorpay_key": "rzp_test_RFCmnFJb7PAojP",
    "amount": amount,
    "order_id": payment["id"]
})

    else:
        form = BookingForm()

    return render(request, "bookingform.html", {"package": package, "form": form})

@login_required
def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.payment_status = "confirmed"
    booking.save()
    return render(request, "confirmation.html", {"booking": booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.payment_status == "pending":
        booking.delete()
    return redirect("cdashboard")


@login_required
def booked_packages(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('package')
    return render(request, 'bookedpackages.html', {'bookings': bookings})
