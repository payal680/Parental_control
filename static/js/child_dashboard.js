setInterval(function(){

loadScreenTime();

},30000);


// -----------------------------
// SIDEBAR 
function openSidebar() {

    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");

    if (sidebar.classList.contains("active")) {
        sidebar.classList.remove("active");
        mainContent.classList.remove("shift");
    } else {
        sidebar.classList.add("active");
        mainContent.classList.add("shift");
    }

}
document.addEventListener("click", function(event) {

    const sidebar = document.getElementById("sidebar");
    const icon = document.querySelector(".profile-icon");
    const mainContent = document.getElementById("main-content");

    if (
        sidebar.classList.contains("active") &&
        !sidebar.contains(event.target) &&
        !icon.contains(event.target)
    ) {
        sidebar.classList.remove("active");
        mainContent.classList.remove("shift");
    }

});
// notifictaion count update
function loadNotifications(){

fetch("/get_notifications/1")

.then(res=>res.json())

.then(data=>{

document.getElementById("notificationCount").innerText = data.length;

})

}

setInterval(loadNotifications,5000);

loadNotifications();
// -----------------------------
// WEEKLY SCREEN TIME BAR GRAPH
// -----------------------------

function loadScreenChart(){

let ctx = document.getElementById("screenChart").getContext("2d");

let weeklyData = [4,5,3,6,4,7,5]; // hours used in week

new Chart(ctx,{

type:"bar",

data:{
labels:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],

datasets:[{
label:"Screen Time (Hours)",
data:weeklyData,
backgroundColor:"blue",
borderRadius:5,
barThickness:40
}]
},

options:{
responsive:true,
maintainAspectRatio:false,

scales:{
y:{
beginAtZero:true,
max:8,
ticks:{
stepSize:1,
callback:function(value){
return value + "h";
}
}
}
},

plugins:{
legend:{
display:false
}
}

}

});

}


// -----------------------------
// APP USAGE PIE CHART
// -----------------------------

function loadAppChart(){

let ctx2 = document.getElementById("appChart").getContext("2d");

// realistic app usage data
let appData = {
"YouTube":120,
"WhatsApp":90,
"Google":60,
"Physics Wallah":150,
"Chrome":50,
"Photos":30,
"Messenger":40
};

let labels = Object.keys(appData);
let values = Object.values(appData);

new Chart(ctx2,{

type:"pie",

data:{
labels:labels,

datasets:[{
data:values,

backgroundColor:[
"red",
"#25D366",
"#4285F4",
"#ff9800",
"#2196f3",
"#9c27b0",
"#00bcd4"
]
}]
},

options:{
responsive:true,
maintainAspectRatio:false
}

});

}


// -----------------------------
// PAGE LOAD
// -----------------------------

window.onload=function(){

loadScreenChart();
loadAppChart();

};










// -----------------------------
// =============================
// GLOBAL VARIABLES
// =============================
// let screenChart;
// let appChart;

// =============================
// LOAD APP USAGE
// =============================
// function loadAppUsage(){

// fetch("/get_app_usage")
// .then(response => response.json())
// .then(data => {

// let labels = [];
// let usage = [];

// data.forEach(app => {
// labels.push(app.app_name);
// usage.push(app.usage_time);
// });

// createAppChart(labels, usage);

// })
// .catch(error => console.error("App Usage Error:", error));

// }

// function createAppChart(labels, usage){

// let ctx = document.getElementById("appChart").getContext("2d");

// if(appChart){
// appChart.destroy();
// }

// appChart = new Chart(ctx,{
// type:"bar",
// data:{
// labels:labels,
// datasets:[{
// label:"Usage Minutes",
// data:usage,
// backgroundColor:"#36a2eb"
// }]
// },
// options:{
// responsive:true
// }
// })

// }


// // =============================
// // ALERT SYSTEM
// // =============================
// function checkAlerts(){

// fetch("/get_alerts/1")
// .then(res => res.json())
// .then(data => {

// if(data.message){

// document.getElementById("messageTitle").innerText = "Alert";
// document.getElementById("messageText").innerText = data.message;

// }

// })
// .catch(error => console.error("Alert Error:", error));

// }


// // =============================
// // LOAD SCREEN TIME
// // =============================
// function loadScreenTime(){

// fetch("/get_screen_time")
// .then(response => response.json())
// .then(data => {

// let screenTime = data.screen_time;

// updateScreenTimeDisplay(screenTime);
// createPieChart(screenTime);
// updateMessage(screenTime);

// })
// .catch(error => console.error("Screen Time Error:", error));

// }


// // =============================
// // UPDATE SCREEN TIME TEXT
// // =============================
// function updateScreenTimeDisplay(time){

// document.getElementById("screenTimeValue").innerText = time;

// }


// // =============================
// // CREATE PIE CHART
// // =============================
// function createPieChart(screenTime){

// let remaining = 180 - screenTime;

// let ctx = document.getElementById("screenChart").getContext("2d");

// if(screenChart){
// screenChart.destroy();
// }

// screenChart = new Chart(ctx,{

// type: "pie",

// data: {
// labels: ["Used Time", "Remaining Time"],
// datasets: [{
// data: [screenTime, remaining],
// backgroundColor: [
// "#ff6384",
// "#36a2eb"
// ]
// }]
// },

// options: {
// responsive: true,
// plugins:{
// legend:{
// position:"bottom"
// }
// }
// }

// });

// }


// // =============================
// // MESSAGE SYSTEM
// // =============================
// function updateMessage(time){

// let title = document.getElementById("messageTitle");
// let text = document.getElementById("messageText");
// let icon = document.getElementById("msgIcon");

// if(time < 60){

// title.innerText = "Excellent Control";
// text.innerText = "Great job! Your screen time is balanced today.";
// icon.innerText = "⭐";

// }
// else if(time < 120){

// title.innerText = "Moderate Usage";
// text.innerText = "You have used your device for a while. Consider taking a break.";
// icon.innerText = "⚡";

// }
// else{

// title.innerText = "High Screen Time";
// text.innerText = "Your screen time is too high today. Try reducing device usage.";
// icon.innerText = "⚠️";

// }

// }


// // =============================
// // SEND APP USAGE DATA
// // =============================
// function sendUsage(appName, usageSeconds){

// fetch("/api/store_usage", {

// method: "POST",

// headers:{
// "Content-Type": "application/json"
// },

// body: JSON.stringify({

// child_id: 1,
// app_name: appName,
// usage_time: usageSeconds,
// date: new Date().toISOString().split("T")[0]

// })

// })

// .then(response => response.json())
// .then(data => console.log("Usage stored:", data))
// .catch(error => console.error("Error:", error));

// }


// // =============================
// // AUTO LOAD WHEN PAGE OPENS
// // =============================
// window.onload = function(){

// loadScreenTime();
// loadAppUsage();
// checkAlerts();

// };


// // =============================
// // AUTO REFRESH EVERY 5 SEC
// // =============================
// setInterval(loadScreenTime, 5000);
// setInterval(loadAppUsage, 5000);
// setInterval(checkAlerts, 5000);