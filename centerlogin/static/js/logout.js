 
document.getElementById("logout").addEventListener("click", function(event) {
    event.preventDefault(); 
    var reallyLogout = confirm("Do you really want to log out?");
    if (reallyLogout) {
        window.location.href =  logoutUrl;
    }
});


 
