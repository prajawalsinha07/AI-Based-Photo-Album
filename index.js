

var apigClient = apigClientFactory.newClient();
window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition

function voiceSearch(){
    if ('SpeechRecognition' in window) {
        console.log("SpeechRecognition is Working");
    } else {
        console.log("SpeechRecognition is Not Working");
    }
    
    var inputSearchQuery = document.getElementById("search_query");
    const recognition = new window.SpeechRecognition();
    //recognition.continuous = true;

    micButton = document.getElementById("mic_search");  
    
    if (micButton.innerHTML == "mic") {
        recognition.start();
    } else if (micButton.innerHTML == "mic_off"){
        recognition.stop();
    }

    recognition.addEventListener("start", function() {
        micButton.innerHTML = "mic_off";
        console.log("Recording.....");
    });

    recognition.addEventListener("end", function() {
        console.log("Stopping recording.");
        micButton.innerHTML = "mic";
    });

    recognition.addEventListener("result", resultOfSpeechRecognition);
    function resultOfSpeechRecognition(event) {
        const current = event.resultIndex;
        transcript = event.results[current][0].transcript;
        inputSearchQuery.value = transcript;
        console.log("transcript : ", transcript)
    }
}




function textSearch() {
    var searchText = document.getElementById('search_query');
    if (!searchText.value) {
        alert('Please enter a valid text or voice input!');
    } else {
        searchText = searchText.value.trim().toLowerCase();
        console.log('Searching Photos....');
        searchPhotos(searchText);
    }
    
}

function searchPhotos(searchText) {

    console.log(searchText);
    document.getElementById('search_query').value = searchText;
    document.getElementById('photos_search_results').innerHTML = "<h4 style=\"text-align:center\">";

    var params = {
        'q' : searchText
    };
    console.log(params)
    apigClient.searchGet(params, {}, {})
        .then(function(result) {
            console.log("Result : ", result);

            image_paths = result["data"]["body"]["imagePaths"];
            console.log("image_paths : ", image_paths);

            var photosDiv = document.getElementById("photos_search_results");
            console.log(photosDiv)
            photosDiv.innerHTML = "";

            var n;
            for (n = 0; n < image_paths.length; n++) {
                images_list = image_paths[n].split('/');
                imageName = images_list[images_list.length - 1];
                console.log(images_list)
                console.log(imageName)

                photosDiv.innerHTML += '<figure><img src="' + image_paths[n] + '" style="width:25%"><figcaption>' + imageName + '</figcaption></figure>';
                console.log(photosDiv.innerHTML)
            }

        }).catch(function(result) {
            console.log(result);
        });
}

function uploadPhoto() {
    var filePath = (document.getElementById('uploaded_file').value).split("\\");
    var fileName = filePath[filePath.length - 1];
    console.log("filePath:" + filePath)
    
    if (!document.getElementById('custom_labels').innerText == "") {
        var customLabels = document.getElementById('custom_labels');
    }
    console.log(fileName);
    console.log(custom_labels.value);

    var reader = new FileReader();
    var file = document.getElementById('uploaded_file').files[0];
    console.log('File : ', file);
    reader.readAsBinaryString(file)
    console.log('File : ', file);
    document.getElementById('uploaded_file').value = "";

    if ((filePath == "") || (!['png', 'jpg', 'jpeg'].includes(fileName.split(".")[1]))) {
        alert("Please upload a valid .png/.jpg/.jpeg file!");
    } else {

        let config = {
            headers: {
                  "Content-Type": file.type,
                  "X-Api-Key": "K8ug9vPmZO3LXNVE3FYBU7jyEz6fcWKy4Mj1CyKC",
                  "x-amz-meta-CustomLabels": custom_labels,
                },
            };
        // var params = {};
        // var additionalParams = {
        //     headers: {
        //         'Access-Control-Allow-Origin': '*',
        //         'Content-Type': file.type
        //     }
        // };

        url = "https://j4gbip87yk.execute-api.us-east-1.amazonaws.com/dev/upload/cloud-project-photos/" + file.name;
          axios.put(url, file, config).then((response) => {
            alert("Upload successful!!");
          });
        
        // reader.onload = function (event) {
        //     console.log(event)
        //     body = btoa(event.target.result);
        //     console.log('Reader body : ', body);
        //     return apigClient.uploadBucketKeyPut(params, body, additionalParams)
        //     .then(function(result) {
        //         console.log(result);
        //     })
        //     .catch(function(error) {
        //         console.log(error);
        //     })
        // }
        // reader.readAsBinaryString(file);
    }
}