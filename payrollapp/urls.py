from django.urls import path
from payrollapp.views import SignupView,LoginView,DueView,ProviderView,InvoiceView,PayrollView,PaidView,PayableView,CredView
urlpatterns = [
    
    #home
    path('home',SignupView.home,name="home"),
    
    #signup
    path('',SignupView.user_signup,name=""),

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

    #update
    path('update',DueView.update,name="update"),


    #provider update data
    path('insurance/update-insurance-status/',ProviderView.vall, name ="update-insurance-status"),


    #save value of bank 
    path('bank/details/',ProviderView.save_val, name ="bank-details"),

    #save value of bank 
    path('payment/details/',ProviderView.pay, name ="paymrnt"),

    #Credential view 
    path('cred',CredView.credential, name ="cred"),


    #Update view 
    path('update/<int:id>',PayrollView.update_date, name ="date_updt"),

    #func2 view
    path('view',PayrollView.func2, name ="view"),


    #calculate amount
    path("amount",PayrollView.get_value, name ="payroll-amount"),
    
    #update amount
    path("drop",PayrollView.option_value, name ="payroll-drop"),


        
    #update payroll amount
    path("get_value",PayrollView.rem_amt, name ="get_value"),
    

    #save payroll amount
    path("save_value",PayrollView.save_data, name ="save_value"),



    #reschedule payroll amount
    path("res_value",PayrollView.data_reschedule, name ="res_value"),
]