(function () {
    "use strict";
    
    let vueapp = Vue.createApp({
        data(){
            return {
		pref_name : "東京都",
                shop_datas : []
            }
        },
        mounted(){
	    this.shop_datas = this.get_pref_data(this.pref_name)
        },
        methods : {
            conv_to_graph_siz(org_val){
		return org_val / 50;
            },

	    get_pref_data(pref){
		return vue_newbuild.get_pref_data(pref)
	    },

            show_jpn_map_modal(){
		alert("HOGE")
                // modal.classList.remove('hidden');
                // mask.classList.remove('hidden');
	    }
        }
    })
    
    class VueNewBuild extends AppBase {
        // constructor() {
        // }
        
        init_page=()=> {
            this.vueapp   = vueapp;
            this.vueapp.mount('#vueapp');
        }

	get_pref_data=(pref)=> {
            let shop_datas = [
                {"shop":"積水ﾊｳｽ",
                 "sold_count":100,     "sold_count_graph":100,
                 "sold_count_diff":10, "sold_count_diff_graph":10,
                 "on_sale_count":100,  "on_sale_count_graph":100,
                 "on_sale_count_diff":10,"on_sale_count_diff_graph":10,
                 "sold_price"   : 50000000,"sold_price_graph" : 50,
                 "on_sale_price": 50000000,"on_sale_price_graph" : 50,
                },
                {"shop":"ｾｷｽｲﾊｲﾑ",
                 "sold_count":100,     "sold_count_graph":100,
                 "sold_count_diff":10, "sold_count_diff_graph":10,
                 "on_sale_count":100,  "on_sale_count_graph":100,
                 "on_sale_count_diff":10,"on_sale_count_diff_graph":10,
                 "sold_price"   : 50000000,"sold_price_graph" : 50,
                 "on_sale_price": 50000000,"on_sale_price_graph" : 50,
                },
                {"shop":"大和ﾊｳｽ",
                 "sold_count":100,     "sold_count_graph":100,
                 "sold_count_diff":10, "sold_count_diff_graph":10,
                 "on_sale_count":100,  "on_sale_count_graph":100,
                 "on_sale_count_diff":10,"on_sale_count_diff_graph":10,
                 "sold_price"   : 50000000,"sold_price_graph" : 50,
                 "on_sale_price": 50000000,"on_sale_price_graph" : 50,
                }
            ];
	    return shop_datas;
        }
	
	// https://qiita.com/ryoyakawai/items/2045e61d417a4b2e819f
	
	get_server_api=(req_path,req_params_hash={})=>{
	    var request = new XMLHttpRequest();

	    req_path_param = req_path;
	    req_params = [];
	    for (let param_key in req_params_hash) {
		req_params.push(encodeURIComponent(param_key)+"="+
				encodeURIComponent(req_params_hash[param_key]))
	    }
	    if ( req_params.length ){
		req_path_param += ( "?"+req_params.join("&") );
	    }

	    request.open("get",req_path_param, true);
	    
	    request.onload = function (event) {
		if (request.readyState === 4) {
		    if (request.status === 200) {
			console.log(request.statusText); // => "OK"
		    } else {
			console.log(request.statusText); // => Error Message
		    }
		}
	    };
	    request.onerror = function (event) {
		console.log(event.type); // => "error"
	    };
	    request.send(null);
	}
	
    }

    window.vue_newbuild = new VueNewBuild();
    vue_newbuild.init_page();

}());

