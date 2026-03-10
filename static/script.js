function startCamera(videoId){

navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{

document.getElementById(videoId).srcObject=stream

})

}