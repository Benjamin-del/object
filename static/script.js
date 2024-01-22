// Setup all elements
const canvas = window.canvas = document.getElementById('canvas');
const video = document.getElementById('videoCam');
const saveBtn = document.getElementById('saveBtn');
const takePhotoBtn = document.getElementById('takePhoto');
const retakeBtn = document.getElementById('retakeBtn');
const response_status = document.getElementById('response');
const uploadBtn = document.getElementById('uploadBtn');
const actBtn = document.getElementById('actBtn');
// Event Divs
const takePhotoDV = document.getElementById('takePhotoDV');
const showPhotoDV = document.getElementById('showPhotoDV');

function uploadPhoto(element) {
    takePhotoDV.style.display = "none"
    showPhotoDV.style.display = "block"

    const reader = new FileReader()
    reader.onload = function(event){
        var img = new Image();
        img.onload = function(){
            canvas.width = img.width;
            canvas.height = img.height;
            canvas.getContext('2d').drawImage(img, 0, 0);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(element.files[0]);    
}
function retakePhoto() {
    // Toggle Elements
    takePhotoDV.style.display = "block"
    showPhotoDV.style.display = "none"
}
async function submitPhoto() {
    // Toggle Elements
    showPhotoDV.style.display = "none"
    takePhotoDV.style.display = "none"

    response_status.style.display = "block"
    response_status.textContent = "Loading..."

    const image = await grabPhoto()
    const formData = new FormData()
    formData.append('file', image)
    const response = await fetch('/upload?dlg=true', {
        method: 'POST',
        body: formData
    });
    const result = await response.json()
    response_status.textContent = result.message
    actBtn.style.display = "block"
    actBtn.textContent = "Retake"
    actBtn.onclick = function () {
        retakePhoto()
        actBtn.style.display = "none"
        response_status.style.display = "none"
    }
}
async function grabPhoto() {
    imageString = canvas.toDataURL("image/jpeg");

    const imageBlobRequest = await fetch(imageString)
    const imageBlob = await imageBlobRequest.blob()
    return imageBlob
}

function takePhoto() {
    // Toggle Elements
    takePhotoDV.style.display = "none"

    showPhotoDV.style.display = "block"

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

}
function openCam() {
    let All_mediaDevices = navigator.mediaDevices
    if (!All_mediaDevices || !All_mediaDevices.getUserMedia) {
        console.log("getUserMedia() not supported.");
        return;
    }
    All_mediaDevices.getUserMedia({
        video: {
            width: {
                min: 1280,
                ideal: 1280,
                max: 1280,
            },
            height: {
                min: 720,
                ideal: 1080,
                max: 1440
            },
            facingMode: 'environment'
        }
    })
        .then(function (vidStream) {
            var video = document.getElementById('videoCam');
            if ("srcObject" in video) {
                video.srcObject = vidStream;
            } else {
                video.src = window.URL.createObjectURL(vidStream);
            }
            video.onloadedmetadata = function (e) {
                video.play();
            };
        })
        .catch(function (e) {
            console.log(e.name + ": " + e.message);
        });
}
openCam()