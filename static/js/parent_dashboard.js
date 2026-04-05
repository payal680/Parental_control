function openSidebar() {
    document.getElementById("sidebar").classList.add("active");
    document.getElementById("main-content").classList.add("shift");
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
// WEEKLY SCREEN TIME BAR GRAPH
// -----------------------------

const weekLabels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];

// screen time hours for demo
const screenData = [3,4,2,5,6,4,3];

const screenCtx = document.getElementById("screenChart").getContext("2d");

new Chart(screenCtx, {
    type: "bar",
    data: {
        labels: weekLabels,
        datasets: [{
            label: "Screen Time (Hours)",
            data: screenData,
            backgroundColor: "#007bff",
            borderRadius: 6,
            barThickness: 40
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 8,
                ticks: {
                    stepSize: 1,
                    callback: function(value){
                        return value + "h";
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
});


// -----------------------------
// APP USAGE PIE CHART
// -----------------------------

const appCtx = document.getElementById("appChart").getContext("2d");

new Chart(appCtx, {
    type: "pie",
    data: {
        labels: [
            "YouTube",
            "WhatsApp",
            "Google",
            "Physics Wallah",
            "Photos",
            "Chrome",
            "Phone"
        ],
        datasets: [{
            data: [35,20,15,10,8,7,5],
            backgroundColor: [
                "#FF0000",
                "#25D366",
                "#4285F4",
                "#FF6B6B",
                "#FFA500",
                "#00BFFF",
                "#6A5ACD"
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: "right"
            }
        }
    }
});



// UPDATE APP LIMIT

function updateLimit(appName,inputId){

let limit=document.getElementById(inputId).value

fetch("/update_limit",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

child_id:1,
app_name:appName,
time_limit:limit

})

})

.then(res=>res.json())

.then(data=>{

alert("Limit Updated")

})

}



window.onload=function(){

loadScreenGraph()
loadAppUsage()

}