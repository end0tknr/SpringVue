"use strict";

let vue_sumstock = Vue.createApp({
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
            town_profiles   : [],
            near_city_profiles : [],
            build_year_profiles: [],
            sort_tbl_dirs : {
                "shop_sales"      : {},
                "shop_city_sales" : {},
                "city_sales"      : {},
                "price_sales"     : {},
                "town_sales"      : {},
                "town_profiles"   : {},
                "near_city_sales" : {},
                "near_city_profiles" : {},
                "build_year_profiles": {}
            },
            show_jpn_map: false,
            disp_date    : "",
            disp_date_min: "",
            disp_date_max: ""
        }
    },
    mounted(){
        this.load_disp_date_range();
    },
    methods : {
        load_disp_date_range(){
            sumstock.load_disp_date_range(this);
            this.load_shops_data(  this.pref_name );
            this.load_cities_data( this.pref_name );
        },

        init_page_by_disp_date(){
            this.load_shops_data(  this.pref_name );
            this.load_cities_data( this.pref_name );
        },
	
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
            this.load_town_profiles(this.pref_name,this.city_name);
            this.load_build_year_profiles(this.pref_name,this.city_name);
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
        
        load_shops_data(pref){
            sumstock.load_shops_data(pref,this);
        },
        load_shop_city_data(pref,city){
            sumstock.load_shop_city_data(pref,city,this);
        },
        load_cities_data(pref,city){
            sumstock.load_cities_data(pref,city,this);
        },
        load_price_data(pref,city){
            sumstock.load_price_data(pref,city,this);
        },
        load_city_profile(pref,city){
            sumstock.load_city_profile(pref,city,this);
        },
        load_near_city_profiles(pref,city){
            sumstock.load_near_city_profiles(pref,city,this);
        },
        load_build_year_profiles(pref,city){
            sumstock.load_build_year_profiles(pref,city,this);
        },
        load_town_data(pref,city){
            sumstock.load_town_data(pref,city,this);
        },
        load_town_profiles(pref,city){
            sumstock.load_town_profiles(pref,city,this);
        },
        load_near_city_data(pref,city){
            sumstock.load_near_city_data(pref,city,this);
        },
        sort_tbl(tbl_name,sort_key){
            if(! this.sort_tbl_dirs[tbl_name][sort_key] ){
                this.sort_tbl_dirs[tbl_name][sort_key] = -1
            }

            this.sort_tbl_dirs[tbl_name][sort_key] *= -1;
            let sort_dir = this.sort_tbl_dirs[tbl_name][sort_key];
            
            this[tbl_name] = sumstock.sort_tbl(this[tbl_name],
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

class SumStock extends NewBuild {
    init_page=()=> {
        this.vueapp   = vue_sumstock;
        this.vueapp.mount('#vueapp');
    }

    server_api_base(){
	return app_conf["api_base_url"] + "sumstock/"
    }
    
    async load_cities_data(pref,city, vue_obj){
        let req_url = this.server_api_base() +"SalesCountByCity/"+
	    encodeURIComponent(pref) + "?date=" + vue_obj.disp_date;
        
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
        vue_obj.load_town_profiles(vue_obj.pref_name,vue_obj.city_name);
        vue_obj.load_near_city_profiles(vue_obj.pref_name,vue_obj.city_name);
        vue_obj.load_build_year_profiles(vue_obj.pref_name,vue_obj.city_name);
    }
    
    build_year_profiles_max_sets(){
        let max_sets = [
            {"key_name" :"damage",
             "max"      :0,
             "atri_keys":["腐朽・破損あり","腐朽・破損なし"]},
            {"key_name" :"reform",
             "max"      :0,
             "atri_keys":["rebuild","reform_plan","reform_kitchen_bath",
                           "reform_roof_outer_wall","reform_floor_inner_wall",
                           "reform_pillar_basic","reform_insulation"] }
            ];
	return max_sets;
    }
    
    async load_build_year_profiles( pref,city,vue_obj ){
        let req_url = this.server_api_base() +"CityProfileByYear/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city)+
	    "?date=" + vue_obj.disp_date;

        let res = await fetch(req_url);
        let city_profiles = await res.json();
        let max_sets = this.build_year_profiles_max_sets();
        
        //最大値算出
        for( let city_profile of city_profiles ) {
            
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( city_profile[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = city_profile[atri_key];
                }
            }
        }
        
        vue_obj.build_year_profiles = [];
        for( let city_profile of city_profiles ) {
            for( let max_set of max_sets ) {
                if ( max_set.max == 0 ){
                    continue
                }

                for( let atri_key of max_set.atri_keys ){
                    let graph_bar_key = atri_key + "_px";

                    city_profile[graph_bar_key] =
                        this.calc_graph_bar_px(city_profile[atri_key],
                                               0,
                                               max_set.max,
                                               50 );
                    //数値の3桁区切り化
                    city_profile[atri_key] =
                        Number(city_profile[atri_key]).toLocaleString();
                }
            }

            vue_obj.build_year_profiles.push( city_profile );
        }
    }
    
}
