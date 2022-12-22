from django.urls import path
from payrollapp.views import SignupView,LoginView,DueView,ProviderView,InvoiceView,PayrollView,PaidView,PayableView
urlpatterns = [
    
    #home
    path('home',SignupView.home,name="home"),
    
    #signup
    path('signup',SignupView.user_signup,name="signup"),

    #login
    path('login',LoginView.user_login,name="login"),

    #logout
    path('logout',LoginView.user_logout,name="logout"),

    # due table 
    path('due',DueView.due_table,name="due"),

    # Provider table 
    path('provider',ProviderView.index,name="provider"),

    # invoice table 
    path('invoice',InvoiceView.invoice,name="invoice"),

    # payroll table 
    path('payroll',PayrollView.payroll,name="payroll"),

    # paid table 
    path('paid',PaidView.paid,name="paid"),

    # payable table 
    path('payable',PayableView.payable,name="payable"),



]