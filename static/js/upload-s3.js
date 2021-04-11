    function getSignedRequest(file){
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4){
                if(xhr.status === 200){
                    var response = JSON.parse(xhr.responseText);
                    uploadFile(file, response.data, response.url);
                }
                else{
                    alert("Could not get signed URL.");
                }
            }
        };
        xhr.send();
    }

    function uploadFile(file, s3Data, url){
        var xhr = new XMLHttpRequest();
        xhr.open("POST", s3Data.url);

        var postData = new FormData();
        for(key in s3Data.fields){
            postData.append(key, s3Data.fields[key]);
        }
        postData.append('file', file);

        xhr.onreadystatechange = function() {
            if(xhr.readyState === 4){
                if(xhr.status === 200 || xhr.status === 204){
                    document.getElementById("builder-preview-img").setAttribute("src", url);
                    document.querySelector('input[name="recipe_img_url"]').setAttribute("value", url);
                    $('#builder-preview-img').attr("src", url).css("display", "block");
                }
                else{
                    alert("Could not upload file.");
                }
            }
        };
        xhr.send(postData);
    }