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
        
    async function checkImage(url) {
        return await makeRequest("GET", url);
    }

    function handle(imgs){
        for (let [key, img] of Object.entries(imgs)){
            
            var url = "../uploads/" + img.getAttribute("alt");
            var preview = document.querySelectorAll('[alt="' + img.getAttribute("alt") + '"][class="recipe-img-header-preview"]')[0];
            img.setAttribute("src", url);
            preview.setAttribute("src", url);
            
            checkImage(url).then(function(result){
                if(result == 200){
                    img.style.display = "block";
                    preview.style.display = "block";
                }
                else {
                    img.style.display = "none";
                    preview.style.display = "none";
                }
            });  
        }
    }