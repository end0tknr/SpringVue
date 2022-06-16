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

    // refer to https://ja.javascript.info/cookie
    
    get_cookie =(name)=> {
        let matches = document.cookie.match(
            new RegExp(
                "(?:^|; )" +
                    name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') +
                    "=([^;]*)"
            ));
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }

    // 使用例:
    // this.set_ookie('user', 'John', {secure: true, 'max-age': 3600});
    set_cookie =( name, value, options={} )=> {

        let default_options = { path: '/'};
        options = Object.assign(default_options, options);

        if (options.expires && options.expires.toUTCString) {
            options.expires = options.expires.toUTCString();
        }

        let updatedCookie =
            encodeURIComponent(name) + "=" + encodeURIComponent(value);

        for (let optionKey in options) {
            updatedCookie += "; " + optionKey;
            let optionValue = options[optionKey];
            if (optionValue !== true) {
                updatedCookie += "=" + optionValue;
            }
        }
        
        document.cookie = updatedCookie;
    }

    del_cookie =(name)=> {
        this.set_cookie(name, "", {'max-age': -1})
    }

}
