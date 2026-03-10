let video=document.getElementById("video")

function startCamera(){

navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{

video.srcObject=stream

})

}


function markAttendance(){

let canvas=document.getElementById("canvas")
let context=canvas.getContext("2d")

context.drawImage(video,0,0,400,300)

let name=document.getElementById("name").value
let roll=document.getElementById("roll").value

fetch("/mark_attendance",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

name:name,
roll:roll

})

})
.then(res=>res.json())
.then(data=>alert(data.message))

}
