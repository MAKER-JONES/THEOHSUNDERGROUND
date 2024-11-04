
let day
window.onload =  function(){
    let today = new Date()
    let date_display = document.getElementById('date')
    if (document.getElementById('lgform').innerText == ''){
        document.getElementById('lgform').remove()
    }


    if(today.getDay() == 1){
        day = 'Monday'
    }else if(today.getDay() == 2){
        day = 'Tuesday'
    }else if(today.getDay() == 3){
        day = 'Wednesday'
    }else if(today.getDay() == 4){
        day = 'Thursday'
    }else if(today.getDay() == 5){
        day = 'Friday'
    }else if(today.getDay() == 6){
        day = 'Saturday'
    }else if(today.getDay() == 0){
        day = 'Sunday'
    }

    if(today.getMonth() == 0){
        month = 'January'
    }else if(today.getMonth() == 1){
        month = 'February'
    }else if(today.getMonth() == 2){
        month = 'March'
    }else if(today.getMonth() == 3){
        month = 'April'
    }else if(today.getMonth() == 4){
        month = 'May'
    }else if(today.getMonth() == 5){
        month = 'June'
    }else if(today.getMonth() == 6){
        month = 'July'
    }else if(today.getMonth() == 7){
        month = 'August'
        
    }else if(today.getMonth() == 8){
        month = 'September'
    }else if(today.getMonth() == 9){
        month = 'October'
    }else if(today.getMonth() == 10){
        month = 'November'
    }else if(today.getMonth() == 11){
        month = 'December'
    }         

    date_display.innerText = day +", "+ month + ' ' + today.getDate() + ', ' + today.getFullYear()
}
let ser = document.getElementById('Search')

function tyFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
    
}
window.onclick = function(event) {
    
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
          ser.classList.toggle("change");
        }
      }
    }
  }
if (document.getElementById('lgform').innerText == 'Logout'){
    document.getElementById('logy').remove()
    document.getElementById('regy').remove()
}else{
    document.getElementById('crea').remove()
}

function mode(typemode){
    if (typemode == 'Category'){
        document.getElementById('typin').hidden = true
        document.getElementById('cat').hidden = false
        document.getElementById('typin').placeholder = typemode
    }else{
        document.getElementById('typin').hidden = false
        document.getElementById('cat').hidden = true
        document.getElementById('typin').placeholder = typemode
    }
    
}
document.getElementById('typin').addEventListener('keydown', function(event){
    if (event.keyCode == 13){
        document.getElementById('searchform').submit()
    }
} )

function catSelect(){
    document.getElementById('searchform').submit()
}
