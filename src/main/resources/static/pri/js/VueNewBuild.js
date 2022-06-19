(function () {
    "use strict";
    //const server_api_base_url = "http://localhost:8080/api/";
    const server_api_base_url = "http://192.168.56.108:8080/pri/js/dummyapi/";
    
    let vueapp = Vue.createApp({
        data(){
            return {
                pref_name : "東京都",
                city_name : "国分寺市",
                shop_sales : [],
                city_sales : [],
                town_sales : [],
                near_city_sales : [],
                sort_tbl_dirs : {
                    "shop_sales"      : {},
                    "city_sales"      : {},
                    "town_sales"      : {},
                    "near_city_sales" : {} }
            }
        },
        mounted(){
            this.load_shop_data(this.pref_name);
            this.load_city_data(this.pref_name);
            this.load_town_data(this.pref_name,this.city_name);
            this.load_near_city_data(this.pref_name,this.city_name);
        },
        methods : {
            conv_to_graph_siz(org_val){
                return org_val / 50;
            },

            load_shop_data(pref){
                vue_newbuild.load_shop_data(pref,this);
            },
            load_city_data(pref){
                vue_newbuild.load_city_data(pref,this);
            },
            load_town_data(pref,city){
                vue_newbuild.load_town_data(pref,city,this);
            },
            load_near_city_data(pref,city){
                vue_newbuild.load_near_city_data(pref,city,this);
            },
            sort_tbl(tbl_name,sort_key){
                if(! this.sort_tbl_dirs[tbl_name][sort_key] ){
                    this.sort_tbl_dirs[tbl_name][sort_key] = -1
                }

                this.sort_tbl_dirs[tbl_name][sort_key] *= -1;
                let sort_dir = this.sort_tbl_dirs[tbl_name][sort_key];
                
                this[tbl_name] = vue_newbuild.sort_tbl(this[tbl_name],
                                                       sort_key,
                                                       sort_dir);
            },
            show_jpn_map_modal(){
                alert("HOGE")
                // modal.classList.remove('hidden');
                // mask.classList.remove('hidden');
            }
        }
    })
    
    class VueNewBuild extends AppBase {
        init_page=()=> {
            this.vueapp   = vueapp;
            this.vueapp.mount('#vueapp');
        }

        sort_tbl(tbl_rows,sort_key,dir){
            tbl_rows = tbl_rows.sort(function(a, b) {
                let val_a = a[sort_key].replace(/,/g,'');
                let val_b = b[sort_key].replace(/,/g,'');
                val_a = Number( val_a );
                val_b = Number( val_b );

                if( isNaN(val_a) ){
                    val_a = a[sort_key];
                }
                if( isNaN(val_b) ){
                    val_b = b[sort_key];
                }
                
                if( val_a < val_b ){
                    return 1 * dir;
                } else if ( val_a > val_b ){
                    return -1 * dir;
                }
                return 0
            });
            return tbl_rows;
        }

        async load_shop_data(pref,vue_obj){
            let req_url = server_api_base_url +
                "newbuild/SalesCountByShop/"+
                encodeURIComponent(pref);
            
            let res = await fetch(req_url);
            let shop_sales = await res.json();
            shop_sales = this.conv_counts_for_disp( shop_sales );
            vue_obj.shop_sales = shop_sales;
        }
        
        async load_city_data(pref,vue_obj){
            let req_url = server_api_base_url +
                "newbuild/SalesCountByCity/"+
                encodeURIComponent(pref);
            
            let res = await fetch(req_url);
            let city_sales = await res.json();
            city_sales = this.conv_counts_for_disp( city_sales );
            vue_obj.city_sales = city_sales;
        }
        
        async load_town_data(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "newbuild/SalesCountByTown/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let town_sales = await res.json();
            town_sales = this.conv_counts_for_disp( town_sales );
            vue_obj.town_sales = town_sales;
        }
        
        async load_near_city_data(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "newbuild/SalesCountByNearCity/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let city_sales = await res.json();
            city_sales = this.conv_counts_for_disp( city_sales );
            vue_obj.near_city_sales = city_sales;
        }
        
        conv_counts_for_disp( sales_counts ){
            let atri_sets = {}
            const atri_keys = ["sold_count",   "sold_price",   "sold_days",
                               "on_sale_count","on_sale_price","on_sale_days"]
            for( let atri_key of atri_keys ) {
                atri_sets[atri_key] = new Set();
            }

            // sort
            sales_counts = sales_counts.sort(function(a, b) {
                for( let atri_key of atri_keys ) {
                    atri_sets[atri_key].add(a[atri_key]);
                    atri_sets[atri_key].add(b[atri_key]);
                }
                
                return b["sold_count"] - a["sold_count"];
            });
            
            let atri_min_max = {}
            for( let atri_key of atri_keys ) {
                let atri_list = Array.from( atri_sets[atri_key] );
                atri_min_max[atri_key] = [Math.min(...atri_list), Math.max(...atri_list)]
            }

            
            for( let sales_count of sales_counts ) {
                for( let atri_key of atri_keys ) {

                    let graph_bar_key = atri_key + "_px";
                    sales_count[graph_bar_key] =
                        this.calc_graph_bar_px(sales_count[atri_key],
                                               atri_min_max[atri_key][0],
                                               atri_min_max[atri_key][1],
                                               50 );

                    //数値の3桁区切り化
                    sales_count[atri_key] = Number(sales_count[atri_key]).toLocaleString();
                }
            }
            return sales_counts;
        }

        calc_graph_bar_px(val, val_min, val_max, bar_max ){
            if(! val ){
                return 0;
            }
            return Math.ceil(val / val_max * bar_max);
        }

    }

    window.vue_newbuild = new VueNewBuild();
    vue_newbuild.init_page();

}());

