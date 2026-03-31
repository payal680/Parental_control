let selectedApp = ""


/* PIE CHART */

function createChart(screenTime){

let remaining = 180 - screenTime

let ctx = document.getElementById("screenChart")

new Chart(ctx,{

type:'pie',

data:{

labels:['Used','Remaining'],

datasets:[{

data:[screenTime,remaining],

backgroundColor:[
'#ff6384',
'#36a2eb'
]

}]

}

})

updateMessage(screenTime)

}



/* MESSAGE SYSTEM */

function updateMessage(time){

let title=document.getElementById("messageTitle")

let box=document.getElementById("messageBox")

if(time < 60){

title.innerHTML="Healthy Digital Habit"

box.innerHTML="Your child is maintaining a balanced screen routine. No action required."

}

else if(time < 120){

title.innerHTML="Moderate Screen Usage"

box.innerHTML="Your child's usage is increasing. Consider monitoring activities."

}

else{

title.innerHTML="High Screen Time Alert"

box.innerHTML="Screen usage has exceeded recommended limits. You may apply restrictions."

}

}



/* LOAD APP LIMITS */

function loadAppLimits(){

fetch("/get_app_limits/1")

.then(res=>res.json())

.then(data=>{

let table=document.getElementById("appsTable")

data.forEach(app=>{

table.innerHTML += `

<tr>

<td>${app.app_name}</td>

<td>${app.time_limit} min</td>

<td>

<button onclick="openLimitModal('${app.app_name}')">

Edit

</button>

</td>

</tr>

`

})

})

}



/* OPEN MODAL */

function openLimitModal(app){

selectedApp=app

document.getElementById("limitModal").style.display="block"

}



/* SAVE LIMIT */

function saveLimit(){

let limit=document.getElementById("limitInput").value

fetch("/update_limit",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

child_id:1,
app_name:selectedApp,
time_limit:limit

})

})

.then(res=>res.json())

.then(data=>{

alert("Limit Updated")

location.reload()

})

}



/* FETCH SCREEN TIME */

fetch("/get_screen_time")

.then(res=>res.json())

.then(data=>{

createChart(data.screen_time)

})


loadAppLimits()