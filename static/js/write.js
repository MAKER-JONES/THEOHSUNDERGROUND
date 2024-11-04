var showingSourceCode = false
var isInEditMode = true
let field = document.getElementById('textfield')
var body = field.contentWindow.document.querySelector('body');
let hasclick = false

body.style.color = 'white'
body.onclick = function(){
    if(hasclick == false){
        //alert('click')
        execCommandWithArg('foreColor', '#e4e2e2')
        hasclick = true
    }
}

body.style.background = 'black'


function editMode(){
    TextField.document.designMode = 'on'
}

function execCmd(command){

    TextField.document.execCommand(command, false, null)
}
function execCommandWithArg(command, arg){
    console.log(arg)
    TextField.document.execCommand(command, false, arg)
}
function toggleSource(){
    if(showingSourceCode){
        TextField.document.getElementsByTagName('body')[0].innerHTML = TextField.document.getElementsByTagName('body')[0].textContent
        //TextField.document.getElementsByTagName('body')[0].classList.add('white')
        showingSourceCode = false
    }else{
        TextField.document.getElementsByTagName('body')[0].textContent = TextField.document.getElementsByTagName('body')[0].innerHTML
        TextField.document.getElementsByTagName('body')[0].style.color = 'white';
        //TextField.document.getElementsByTagName('body')[0].classList.add('white')
        showingSourceCode = true
    }
}

function toggleEdit(){
    if(isInEditMode){
        
        field.classList.add('normal')
        
        
        

        TextField.document.designMode = 'off'
        //body.style.color = 'white';
        body.style.background = 'black'
        var nodes = field.childNodes;
        for(var i=0; i<nodes.length; i++) {
            if (nodes[i].nodeName.toLowerCase() == 'div') {
                nodes[i].style.background = 'black';
               
            }
        }
        isInEditMode = false
    }else{
        
        
        field.classList.remove('normal')
        
        TextField.document.designMode = 'on'
        
        isInEditMode = true
    }
}

let day
window.onload =  function(){
    
    let today = new Date()
    let date_display = document.getElementById('date')


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

function submit_article(){
    document.getElementById('subbutton').disabled = true
    if(showingSourceCode){
        TextField.document.getElementsByTagName('body')[0].innerHTML = TextField.document.getElementsByTagName('body')[0].textContent
        showingSourceCode = false
    }

    let article = TextField.document.getElementsByTagName('body')[0].innerHTML
    console.log(article)
    if (article.indexOf('script') > -1){
        alert("not allowed to add script");
        document.getElementById('subbutton').disabled = false
    }else if( document.getElementById('titlein').value==''){

        alert('must fill out title')
        document.getElementById('subbutton').disabled = false
    }else if(document.getElementById('cat').value == 'Category'){
        alert('must pick category')
        document.getElementById('subbutton').disabled = false
    }else if(document.getElementById('dataurl').value == ''){
        alert('must select thumnail')
        document.getElementById('subbutton').disabled = false
    }else{
        document.getElementById('post_article').setAttribute('value', article)
        document.getElementById('inform').submit()
    }

    
    
    //let article = document.getElementById('post_article').in

}


function readURL(input) {
    document.getElementById('flab').innerText = 'Thumbnail Selected'
    var reader = new FileReader();
		
    reader.addEventListener("load", function() {
        
        var src = reader.result;
        console.log(src)
        document.getElementById('dataurl').value = src
        

        
      });

    reader.readAsDataURL(input.files[0])
  
}