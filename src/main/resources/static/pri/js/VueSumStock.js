(function () {
    "use strict";
    const server_api_base_url = "http://localhost:8080/api/";
    //const server_api_base_url = "http://192.168.56.108:8080/pri/js/dummyapi/";
    
    let vueapp = Vue.createApp({
        data(){
            return {
                pref_name : "東京都",
                city_name : "",
                shop_sales      : [],
                city_sales      : [],
                price_sales     : [],
                shop_city_sales : [],
                town_sales      : [],
                near_city_sales : [],
                city_profile    : {},
                near_city_profiles : [],
                sort_tbl_dirs : {
                    "shop_sales"      : {},
                    "shop_city_sales" : {},
                    "city_sales"      : {},
                    "price_sales"     : {},
                    "town_sales"      : {},
                    "near_city_sales" : {},
                    "near_city_profiles" : {} },
                show_jpn_map: false
            }
        },
        mounted(){
            this.load_shops_data(this.pref_name);
            this.load_cities_data(this.pref_name);
        },
        methods : {
            load_city_datas(pref_name, city_name){
                
                if ( this.pref_name != pref_name){
                    this.pref_name = pref_name;
                    this.load_shops_data(this.pref_name);
                    this.load_cities_data(this.pref_name, city_name);
                    return;
                }
          
                this.city_name = city_name;
                this.load_shop_city_data(this.pref_name,this.city_name);
                this.load_town_data(this.pref_name,this.city_name);
                this.load_near_city_data(this.pref_name,this.city_name);
                this.load_price_data(this.pref_name,this.city_name);
                this.load_city_profile(this.pref_name,this.city_name);
                this.load_near_city_profiles(this.pref_name,this.city_name);
            },
            
            set_pref_name(event){
                if( event.target.className != "pref"){
                    return;
                }
                
                let pref = event.target.innerText;
                if (! pref ){
                    return;
                }
                
                if ( pref =="東京"){
                    pref += "都"
                } else if( pref=="北海道"){
                    
                } else if( pref=="京都" || pref=="大阪"){
                    pref += "府"
                } else {
                    pref += "県"
                }
                this.pref_name = pref;
                
                this.load_shops_data(this.pref_name);
                this.load_cities_data(this.pref_name);
                
                this.hide_jpn_map_modal();
            },
            
            conv_to_graph_siz(org_val){
                return org_val / 50;
            },

            load_shops_data(pref){
                vue_sumstock.load_shops_data(pref,this);
            },
            load_shop_city_data(pref,city){
                vue_sumstock.load_shop_city_data(pref,city,this);
            },
            load_cities_data(pref,city){
                vue_sumstock.load_cities_data(pref,city,this);
            },
            load_price_data(pref,city){
                vue_sumstock.load_price_data(pref,city,this);
            },
            load_city_profile(pref,city){
                vue_sumstock.load_city_profile(pref,city,this);
            },
            load_near_city_profiles(pref,city){
                vue_sumstock.load_near_city_profiles(pref,city,this);
            },
            load_town_data(pref,city){
                vue_sumstock.load_town_data(pref,city,this);
            },
            load_near_city_data(pref,city){
                vue_sumstock.load_near_city_data(pref,city,this);
            },
            sort_tbl(tbl_name,sort_key){
                if(! this.sort_tbl_dirs[tbl_name][sort_key] ){
                    this.sort_tbl_dirs[tbl_name][sort_key] = -1
                }

                this.sort_tbl_dirs[tbl_name][sort_key] *= -1;
                let sort_dir = this.sort_tbl_dirs[tbl_name][sort_key];
                
                this[tbl_name] = vue_sumstock.sort_tbl(this[tbl_name],
                                                       sort_key,
                                                       sort_dir);
            },
            show_jpn_map_modal(){
                this.show_jpn_map = true;
            },
            hide_jpn_map_modal(){
                this.show_jpn_map = false;
            }
        }
    })
    
    class VueSumStock extends AppBase {
        init_page=()=> {
            this.vueapp   = vueapp;
            this.vueapp.mount('#vueapp');
        }

        sort_tbl(tbl_rows,sort_key,dir){
            tbl_rows = tbl_rows.sort(function(a, b) {
                if(a[sort_key]==undefined && b[sort_key]==undefined ){
                    return 0;
                }
                if(a[sort_key]!=undefined && b[sort_key]==undefined ){
                    return 1 * dir;
                }
                if(a[sort_key]==undefined && b[sort_key]!=undefined ){
                    return -1 * dir;
                }
                
                let val_a = a[sort_key];
                let val_b = b[sort_key];
		
		if (typeof val_a != 'number'){
                    val_a = Number( val_a.replace(/,/g,'') );
		}
		if (typeof val_b != 'number'){
                    val_b = Number( val_b.replace(/,/g,'') );
		}

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

        async load_shops_data(pref,vue_obj){
            let req_url = server_api_base_url +
                "sumstock/SalesCountByShop/"+
                encodeURIComponent(pref);
            
            let res = await fetch(req_url);
            let shop_sales = await res.json();
            shop_sales = this.conv_counts_for_disp( shop_sales );
            vue_obj.shop_sales = shop_sales;
        }
        
        async load_cities_data(pref,city, vue_obj){
            let req_url = server_api_base_url +
                "sumstock/SalesCountByCity/"+
                encodeURIComponent(pref);
            
            let res = await fetch(req_url);
            let city_sales = await res.json();
            city_sales = this.conv_counts_for_disp( city_sales );
            vue_obj.city_sales = city_sales;

            if( city ){
                vue_obj.city_name = city;
            } else {
                vue_obj.city_name = city_sales[0].city;
            }
            
            vue_obj.load_shop_city_data(vue_obj.pref_name,vue_obj.city_name);
            vue_obj.load_town_data(vue_obj.pref_name,vue_obj.city_name);
            vue_obj.load_near_city_data(vue_obj.pref_name,vue_obj.city_name);
            vue_obj.load_price_data(vue_obj.pref_name,vue_obj.city_name);
            vue_obj.load_city_profile(vue_obj.pref_name,vue_obj.city_name);
            vue_obj.load_near_city_profiles(vue_obj.pref_name,vue_obj.city_name);
        }
        
        async load_town_data(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "sumstock/SalesCountByTown/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let town_sales = await res.json();
            town_sales = this.conv_counts_for_disp( town_sales );
            vue_obj.town_sales = town_sales;
        }
        
        async load_shop_city_data(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "sumstock/SalesCountByShopCity/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let town_sales = await res.json();
            town_sales = this.conv_counts_for_disp( town_sales );
            vue_obj.shop_city_sales = town_sales;
        }
        
        async load_price_data(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "sumstock/SalesCountByPrice/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let price_sales = await res.json();
            price_sales = this.conv_counts_for_disp( price_sales );
            vue_obj.price_sales = price_sales;
        }
        
        async load_near_city_profiles(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "sumstock/NearCityProfiles/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let city_profiles = await res.json();
            vue_obj.near_city_profiles = [];
            for( let city_profile of city_profiles ) {
                city_profile = JSON.parse( city_profile );

                city_profile["戸建率"] =
                    city_profile["世帯_戸建"] /
                    (city_profile["世帯_戸建"] + city_profile["世帯_集合"]);
                city_profile["戸建率"] = Math.round(city_profile["戸建率"] *100);
                
                city_profile["持家率"] =
                    city_profile["世帯_持家"] /
                    (city_profile["世帯_持家"] + city_profile["世帯_賃貸"]);
                city_profile["持家率"] = Math.round(city_profile["持家率"] *100);
                
                for (let atri_key in city_profile){
                    if (atri_key in ["持家率","戸建率"]){
                        continue
                    }
                    
                    city_profile[atri_key] = city_profile[atri_key].toLocaleString();
                }
                vue_obj.near_city_profiles.push(city_profile);
            }
        }
        
        async load_city_profile(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "sumstock/CityProfile/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let city_profile = await res.json();

            city_profile["戸建率"] =
                city_profile["世帯_戸建"] /
                (city_profile["世帯_戸建"] + city_profile["世帯_集合"]);
            city_profile["戸建率"] = Math.round(city_profile["戸建率"] *100);
            
            city_profile["持家率"] =
                city_profile["世帯_持家"] /
                (city_profile["世帯_持家"] + city_profile["世帯_賃貸"]);
            city_profile["持家率"] = Math.round(city_profile["持家率"] *100);

            let tmp_sum =
                city_profile["入手_分譲"] + city_profile["入手_新築"] + city_profile["入手_建替"];
            
            city_profile["入手_分譲"] = Math.round(city_profile["入手_分譲"] / tmp_sum *100);
            city_profile["入手_新築"] = Math.round(city_profile["入手_新築"] / tmp_sum *100);
            city_profile["入手_建替"] = Math.round(city_profile["入手_建替"] / tmp_sum *100);

            let atri_keys =
                ["人口_20_24歳_万人","人口_25_59歳_万人",,"人口_60歳_万人",
                 "総世帯","家族世帯","単身世帯"]
            for( let atri_key of atri_keys ) {
                city_profile[atri_key+"_差"] =
                    city_profile[atri_key] - city_profile[atri_key+"_2015"];
                city_profile[atri_key+"_差"] =
                    city_profile[atri_key+"_差"].toLocaleString();
                if(! city_profile[atri_key+"_差"]){
                    city_profile[atri_key+"_差"] = "±0"
                } else if (city_profile[atri_key+"_差"].indexOf("-") < 0 ){
                    city_profile[atri_key+"_差"] =
                        "+"+ city_profile[atri_key+"_差"];
                }
            }

            atri_keys = ["総世帯","家族世帯","単身世帯","生産緑地_ha",
                         "用途地域_住居系_ha","用途地域_商業系_ha"]
            for( let atri_key of atri_keys ) {
                if (! city_profile[atri_key]) {
                    continue
                }
                city_profile[atri_key] =
                    city_profile[atri_key].toLocaleString();
            }
            city_profile["mapexpert_id"] =
                city_profile["citycode"].substr( 0, city_profile["citycode"].length-1 );

            
            //console.log(city_profile);
            vue_obj.city_profile = city_profile;
        }
        
        async load_near_city_data(pref,city,vue_obj){
            let req_url = server_api_base_url +
                "sumstock/SalesCountByNearCity/"+
                encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
            
            let res = await fetch(req_url);
            let city_sales = await res.json();
            city_sales = this.conv_counts_for_disp( city_sales );
            vue_obj.near_city_sales = city_sales;
        }
        
        conv_counts_for_disp( sales_counts ){
            // 最大/最小値を算出する為の準備
            let atri_sets = {}
            const atri_keys = ["sold_count",   "sold_price",   "sold_days",
                               "on_sale_count","on_sale_price","on_sale_days"]
            
            for( let atri_key of atri_keys ) {
                atri_sets[atri_key] = new Set();
            }

            for( let sales_count of sales_counts ) {
                // 円→百万円
                for( let atri_key of ["sold_price","on_sale_price"] ) {
                    sales_count[atri_key] =
                        Math.round(sales_count[atri_key] /1000000)
                }
                
                for( let atri_key of atri_keys ) {
                    atri_sets[atri_key].add( sales_count[atri_key] );
                }
            }
        
            // sort
            sales_counts = sales_counts.sort(function(a, b) {
                return b["on_sale_count"] - a["on_sale_count"];
            });
            
            let atri_min_max = {}
            for( let atri_key of atri_keys ) {
                let atri_list = Array.from( atri_sets[atri_key] );
                atri_min_max[atri_key] =
                    [Math.min(...atri_list), Math.max(...atri_list)]
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
                    sales_count[atri_key] =
                        Number(sales_count[atri_key]).toLocaleString();
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

    window.vue_sumstock = new VueSumStock();
    vue_sumstock.init_page();
}());
