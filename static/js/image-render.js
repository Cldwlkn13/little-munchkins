    function makeRequest(method, url) {
        return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
                if (this.status >= 200 && this.status < 300) {
                    resolve(this.status);
                } 
                else {
                    reject({
                            status: this.status,
                            statusText: xhr.statusText
                        });
                    }
                };
                xhr.onerror = function () {
                    reject({
                        status: this.status,
                        statusText: xhr.statusText
                    });
                };
                xhr.send();
            });
    }
        
    async function checkImage(img, preview, img_url) {
        
        var filename = img_url.replace(/^.*[\\\/]/, '')
        var url = "../get_s3/" + filename;

        img.setAttribute("src", img_url);
        preview.setAttribute("src", img_url);
        
        return await makeRequest("GET", url);
    }

    function handle(imgs){
        for (let [key, img] of Object.entries(imgs)){
            var img_url = img.getAttribute("alt");
            if(img_url == ""){
                return;
            }
            var preview = document.querySelectorAll('[alt="' + img.getAttribute("alt") + '"][class="recipe-img-header-preview"]')[0];
            checkImage(img, preview, img_url)
                .then(result => {
                    if(result >= 200 && result < 300){
                        img.style.display = "block";
                        preview.style.display = "block";
                    }
                    else {
                        img.style.display = "none";
                        preview.style.display = "none";
                    }
                }).catch(reject => {
                    img.style.display = "none";
                    preview.style.display = "none";
                });  
        }
    }