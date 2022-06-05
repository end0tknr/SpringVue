'use strict';
class AppBase {
    
    constructor() {}
    
    error_to_server =(err_msg)=> {
        // console.log(err_msg);
        const xhr = new XMLHttpRequest();
        const url = `/error_js.html?msg=` + encodeURI(err_msg);
        xhr.open("GET", url, true);
        xhr.send();
    }

    // refer to https://stackoverflow.com/questions/51843227
    get_latlng=()=>{
        return new Promise( (resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                position => resolve(position),
                error => reject(error)
            )
        })
    }
}
