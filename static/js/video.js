 
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


function previewFile(){
    const preview = document.querySelector('video')
    const file = document.getElementById('videoInput').files[0]
    
    const reader = new FileReader()
    

    reader.addEventListener('load', function(){
        preview.src = reader.result
        preview.hidden = false
        document.getElementById('videoBlob').value = reader.result

    }, false)
    if(file){
        reader.readAsDataURL(file)
    }else{
        preview.src = 'unknown'
    }
    
    document.getElementById
    
}
function readURL(input) {
    document.getElementById('flab').innerText = 'Thumbnail Selected'
    var reader = new FileReader();
		
    reader.addEventListener("load", function() {
        
        var src = reader.result;
        document.getElementById('thumbnailSRC').setAttribute('value', src)
        

        
      });

    reader.readAsDataURL(input.files[0])
  
}
function submit_article(){
    if( document.getElementById('titlein').value==''){
        alert('must fill out title')
    }else if(document.getElementById('cat').value == 'Category'){
        alert('must pick category')
    }else if(document.getElementById('thumbnailSRC').value == ''){
        alert('must select thumnail')
    }else if(document.getElementById('videoBlob').value == ''){
        alert('no video inserted')

        
    }else if(document.getElementById('videoBlob').value == '(unknown)'){
        alert('invalid video, make sure video is in mp4 format')

    }else{
        
        
        document.getElementById('inform').submit()
    }
    
    

}