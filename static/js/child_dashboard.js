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
// -----------------------------

let chart;


// -----------------------------
// FETCH SCREEN TIME FROM SERVER
// -----------------------------

function loadScreenTime(){

fetch("/get_screen_time")

.then(response => response.json())

.then(data => {

let screenTime = data.screen_time;

updateScreenTimeDisplay(screenTime);

createPieChart(screenTime);

updateMessage(screenTime);

})

.catch(error => console.error("Error:", error));

}



// -----------------------------
// UPDATE SCREEN TIME TEXT
// -----------------------------

function updateScreenTimeDisplay(time){

document.getElementById("screenTimeValue").innerText = time;

}



// -----------------------------
// CREATE PIE CHART
// -----------------------------

function createPieChart(screenTime){

let remaining = 180 - screenTime;

let ctx = document.getElementById("screenChart").getContext("2d");

if(chart){
chart.destroy();
}

chart = new Chart(ctx,{

type: "pie",

data: {

labels: ["Used Time", "Remaining Time"],

datasets: [{

data: [screenTime, remaining],

backgroundColor: [
"#ff6384",
"#36a2eb"
]

}]

},

options: {

responsive: true,

plugins: {
legend: {
position: "bottom"
}
}

}

});

}



// -----------------------------
// MESSAGE SYSTEM
// -----------------------------

function updateMessage(time){

let title = document.getElementById("messageTitle");

let text = document.getElementById("messageText");

let icon = document.getElementById("msgIcon");

if(time < 60){

title.innerText = "Excellent Control";

text.innerText = "Great job! Your screen time is balanced today.";

icon.innerText = "⭐";

}

else if(time < 120){

title.innerText = "Moderate Usage";

text.innerText = "You have used your device for a while. Consider taking a break.";

icon.innerText = "⚡";

}

else{

title.innerText = "High Screen Time";

text.innerText = "Your screen time is too high today. Try reducing device usage.";

icon.innerText = "⚠️";

}

}



// -----------------------------
// SEND APP USAGE DATA TO FLASK
// -----------------------------

function sendUsage(appName, usageSeconds){

fetch("/api/store_usage", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({

child_id: 1,
app_name: appName,
usage_time: usageSeconds,
date: new Date().toISOString().split("T")[0]

})

})

.then(response => response.json())

.then(data => console.log("Usage stored:", data))

.catch(error => console.error("Error:", error));

}


