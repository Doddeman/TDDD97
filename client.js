displayView = function(view){
 // the code required to display a view
 document.getElementById("clientviewer").innerHTML = view;
};
window.onload = function(){
 //code that is executed as the page is loaded.
 //You shall put your own custom code here.
 //window.alert() is not allowed to be used in your implementation.
 
    welcomeview  = document.getElementById('welcomeview').innerHTML;
    
    displayView(welcomeview);
};
