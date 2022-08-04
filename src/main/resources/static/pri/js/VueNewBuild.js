"use strict";
    
let vue_newbuild = Vue.createApp({
    data(){
        return {
            pref_name : "",
            city_name : "",
            shop_sales            : [],
            shop_scale_sales      : [],
            shop_city_sales       : [],
            shop_city_scale_sales : [],
            city_sales            : [],
            city_scale_sales      : [],
            price_sales           : [],
            town_sales            : [],
            town_scale_sales      : [],
            near_city_sales       : [],
            city_profile          : {},
            city_ratings          : [],
            town_profile          : [],
            town_profiles         : [],
            town_ratings          : [],
            near_city_profiles    : [],
            build_year_profiles   : [],
            sort_tbl_dirs : {
                "shop_sales"            : {},
                "shop_scale_sales"      : {},
                "shop_city_sales"       : {},
                "shop_city_scale_sales" : {},
                "city_sales"            : {},
                "city_scale_sales"      : {},
                "city_ratings"          : {},
                "price_sales"           : {},
                "town_sales"            : {},
                "town_scale_sales"      : {},
                "town_profiles"         : {},
                "town_ratings"          : {},
                "near_city_sales"       : {},
                "near_city_profiles"    : {},
                "build_year_profiles"   : {} },
            show_jpn_map: false,
            show_gps    : false,
            disp_date    : "",
            disp_date_min: "",
            disp_date_max: ""
        }
    },
    mounted(){
        newbuild.load_disp_date_range(this);
        newbuild.chk_client(this);
    },
    methods : {

        init_page_by_disp_date(){
            newbuild.load_shops_data(this.pref_name,this);
            newbuild.load_shop_scale_data(this.pref_name,this);
            newbuild.load_cities_data(this.pref_name,this);
            newbuild.load_city_scale_data(this.pref_name,this);
	    
            this.load_city_datas(this.pref_name, this.city_name );
        },
        
        load_city_datas(pref_name, city_name){
            
            if ( this.pref_name != pref_name){
                this.pref_name = pref_name;
                newbuild.load_shops_data(pref,this);
                newbuild.load_shop_scale_data(pref,this);
                newbuild.load_cities_data(pref,city,this);
                return;
            }
            
            this.city_name = city_name;
            newbuild.load_shop_city_data(pref_name,city_name,this);
            newbuild.load_shop_city_scale_data(pref_name,city_name,this);
            newbuild.load_near_city_data(pref_name,city_name,this);
            newbuild.load_price_data(pref_name,city_name,this);
            newbuild.load_city_profile(pref_name,city_name,this);
            newbuild.load_city_ratings(pref_name,this);
            newbuild.load_town_data(pref_name,city_name,this);
            newbuild.load_town_scale_data(pref_name,city_name,this);
            newbuild.load_town_profiles(pref_name,city_name,this);
            newbuild.load_town_ratings(pref_name,city_name,this);
            newbuild.load_near_city_profiles(pref_name,city_name,this);
            newbuild.load_build_year_profiles(pref_name,city_name,this);
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

            newbuild.load_shops_data(pref,this);
            newbuild.load_shop_scale_data(pref,this);
            newbuild.load_cities_data(pref,this);
            newbuild.load_city_scale_data(pref,this);
            this.hide_jpn_map_modal();
        },
        
        sort_tbl(tbl_name,sort_key){
            if(! this.sort_tbl_dirs[tbl_name][sort_key] ){
                this.sort_tbl_dirs[tbl_name][sort_key] = -1
            }
            
            this.sort_tbl_dirs[tbl_name][sort_key] *= -1;
            let sort_dir = this.sort_tbl_dirs[tbl_name][sort_key];
            
            this[tbl_name] = newbuild.sort_tbl(this[tbl_name],
                                               sort_key,
                                               sort_dir);
        },
        show_gps_modal(){
            this.show_gps = true;
        },
        hide_gps_modal(){
            this.show_gps = false;
        },
        show_jpn_map_modal(){
            this.show_jpn_map = true;
        },
        hide_jpn_map_modal(){
            this.show_jpn_map = false;
        }
    }
})

class NewBuild extends AppBase {
    init_page=()=> {
        this.vueapp   = vue_newbuild;
        this.vueapp.mount('#vueapp');
    }
    
    server_api_base(){
        return app_conf["api_base_url"] + "newbuild/"
    }
    
    async chk_client(vue_obj){
        let ret_pos = await this.load_client_ip();
        if(ret_pos.ip_type=="private"){
            vue_obj.show_jpn_map_modal();
            return;
        }

        vue_obj.show_gps_modal();
        
        let latlng_pos;
        try {
            latlng_pos = await this.get_latlng();
        } catch(err) {
            let error_msg = ["chk_client()",
                             "err_code=",
                             err.code,
                             err.message].join(" ");
            this.error_to_server( error_msg );
            return;
        }

        let req_url = this.server_api_base() + "CityByLatLng/"+
            latlng_pos.coords.latitude +","+latlng_pos.coords.longitude;
        let res = await fetch(req_url);
        let pref_city = await res.json();
        
        vue_obj.pref_name = pref_city["pref"];

        this.load_shops_data(vue_obj.pref_name, vue_obj);
        this.load_shop_scale_data(vue_obj.pref_name, vue_obj);
        this.load_cities_data(vue_obj.pref_name,vue_obj);
        this.load_city_scale_data(vue_obj.pref_name,vue_obj);
        vue_obj.hide_gps_modal();
    }
    
    async load_client_ip(){
        let req_url = this.server_api_base() + "ClientIp";
        let res = await fetch(req_url);
        let client_ip = await res.json();
        return client_ip;
    }
    
    async load_disp_date_range(vue_obj){
        let req_url = this.server_api_base() + "DispDateRange";

        let res = await fetch(req_url);
        let disp_dates = await res.json();
        vue_obj.disp_date_min = disp_dates[0];
        vue_obj.disp_date_max = disp_dates[1];
        vue_obj.disp_date     = disp_dates[1];
    }
    
    async load_shops_data(pref,vue_obj){
        let req_url = this.server_api_base() + "SalesCountByShop/"+
            encodeURIComponent(pref) + "?date=" + vue_obj.disp_date;

        let res = await fetch(req_url);
        let shop_sales = await res.json();
        shop_sales = this.conv_counts_for_disp( shop_sales );
        vue_obj.shop_sales = shop_sales;
    }
    
    async load_shop_scale_data(pref,vue_obj){
        let req_url = this.server_api_base() + "SalesCountByShopScale/"+
            encodeURIComponent(pref) + "?date=" + vue_obj.disp_date;

        let res = await fetch(req_url);
        let scale_sales = await res.json();
        let max_sets = this.scale_sales_max_sets();
        
        let scale_sales_tmp = [];
        for( let scale_sale of scale_sales ) {
            scale_sale = JSON.parse( scale_sale );
            
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( scale_sale[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = scale_sale[atri_key];
                }
            }
            scale_sales_tmp.push( scale_sale );
        }
        
        scale_sales = this.conv_scale_counts_for_disp( scale_sales_tmp );
        vue_obj.shop_scale_sales = scale_sales;
    }
    
    async load_city_scale_data(pref,vue_obj){
        let req_url = this.server_api_base() + "SalesCountByCityScale/"+
            encodeURIComponent(pref) + "?date=" + vue_obj.disp_date;

        let res = await fetch(req_url);
        let scale_sales = await res.json();
        let max_sets = this.scale_sales_max_sets();
        
        let scale_sales_tmp = [];
        for( let scale_sale of scale_sales ) {
            scale_sale = JSON.parse( scale_sale );
            
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( scale_sale[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = scale_sale[atri_key];
                }
            }
            scale_sales_tmp.push( scale_sale );
        }
        
        scale_sales = this.conv_scale_counts_for_disp( scale_sales_tmp );
        vue_obj.city_scale_sales = scale_sales;
    }
    
    async load_cities_data(pref,vue_obj){
        let req_url = this.server_api_base() +"SalesCountByCity/"+
            encodeURIComponent(pref) + "?date=" + vue_obj.disp_date;
        
        let res = await fetch(req_url);
        let city_sales = await res.json();
        city_sales = this.conv_counts_for_disp( city_sales );
        vue_obj.city_sales = city_sales;
        
        vue_obj.city_name = city_sales[0].city;


        let pref_name = vue_obj.pref_name;
        let city_name = vue_obj.city_name;
        this.load_shop_city_data(pref_name, city_name, vue_obj);
        this.load_shop_city_scale_data(pref_name,city_name,vue_obj);
        this.load_near_city_data(pref_name,city_name,vue_obj);
        this.load_price_data(pref_name,city_name,vue_obj);
        this.load_city_profile(pref_name,city_name,vue_obj);
        this.load_city_ratings(pref_name,vue_obj);
        this.load_near_city_profiles(pref_name,city_name,vue_obj);
        this.load_town_data(pref_name,city_name,vue_obj);
        this.load_build_year_profiles(pref_name,city_name,vue_obj);
        this.load_town_scale_data(pref_name,city_name,vue_obj);
        this.load_town_profiles(pref_name,city_name,vue_obj);
        this.load_town_ratings(pref_name,city_name,vue_obj);
    }
    
    async load_town_data(pref,city,vue_obj){
        let req_url = this.server_api_base() +"SalesCountByTown/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city)+
            "?date=" + vue_obj.disp_date;
        
        let res = await fetch(req_url);
        let town_sales = await res.json();
        town_sales = this.conv_counts_for_disp( town_sales );
        vue_obj.town_sales = town_sales;
    }
    
    async load_town_scale_data(pref,city, vue_obj){
        let req_url = this.server_api_base() + "SalesCountByTownScale/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city)
            + "?date=" + vue_obj.disp_date;

        let res = await fetch(req_url);
        let scale_sales = await res.json();
        let max_sets = this.scale_sales_max_sets();
        
        let scale_sales_tmp = [];
        for( let scale_sale of scale_sales ) {
            scale_sale = JSON.parse( scale_sale );
            
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( scale_sale[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = scale_sale[atri_key];
                }
            }
            scale_sales_tmp.push( scale_sale );
        }
        
        scale_sales = this.conv_scale_counts_for_disp( scale_sales_tmp );
        vue_obj.town_scale_sales = scale_sales;
    }
    
    async load_shop_city_scale_data(pref,city, vue_obj){
        let req_url = this.server_api_base() + "SalesCountByShopCityScale/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city)
            + "?date=" + vue_obj.disp_date;

        let res = await fetch(req_url);
        let scale_sales = await res.json();
        let max_sets = this.scale_sales_max_sets();
        
        let scale_sales_tmp = [];
        for( let scale_sale of scale_sales ) {
            scale_sale = JSON.parse( scale_sale );
            
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( scale_sale[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = scale_sale[atri_key];
                }
            }
            scale_sales_tmp.push( scale_sale );
        }
        
        scale_sales = this.conv_scale_counts_for_disp( scale_sales_tmp );
        vue_obj.shop_city_scale_sales = scale_sales;
    }
    
    async load_shop_city_data(pref,city,vue_obj){
        let req_url = this.server_api_base() +"SalesCountByShopCity/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city)+
            "?date=" + vue_obj.disp_date;
        
        let res = await fetch(req_url);
        let town_sales = await res.json();
        town_sales = this.conv_counts_for_disp( town_sales );
        vue_obj.shop_city_sales = town_sales;
    }
    
    async load_price_data(pref,city,vue_obj){
        let req_url = this.server_api_base() +"SalesCountByPrice/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city) +
            "?date=" + vue_obj.disp_date;
        
        let res = await fetch(req_url);
        let price_sales = await res.json();
        price_sales = this.conv_price_counts_for_disp( price_sales );
        vue_obj.price_sales = price_sales;
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
        let req_url = this.server_api_base() +"CityProfileByBuildYear/"+
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
    
    near_city_profiles_max_sets(){
        let max_sets = [
            {"key_name" :"pop", "max":0,
             "atri_keys":['人口_25_59歳_万人']},
            {"key_name" :"pop_diff", "max":0,
             "atri_keys":['人口_25_59歳_万人_変動']},
            {"key_name" :"setai", "max":0,
             "atri_keys":['家族世帯','単身世帯']},
            {"key_name" :"setai_diff", "max":0,
             "atri_keys":['家族世帯_変動','単身世帯_変動']},
            {"key_name" :"area", "max":0,
             "atri_keys":['用途地域_住居系_ha']},
            {"key_name" :"chika", "max":0,
             "atri_keys":['地価_万円_m2_住居系']},
            {"key_name" :"owned", "max":0,
             "atri_keys":['持家率']},
            {"key_name" :"house", "max":0,
             "atri_keys":['戸建率']},
            {"key_name" :"person_income", "max":0,
             "atri_keys":['年収_百万円']}
        ];
        return max_sets;
    }

    ratings_max_sets(){
        let max_sets = [
            {"key_name":"ss_sold_count",  "max":0,"atri_keys":['ss_sold_count']},
            {"key_name":"ss_onsale_shop", "max":0,"atri_keys":['ss_onsale_shop']},
            {"key_name":"ss_onsale_count","max":0,"atri_keys":['ss_onsale_count']},
            {"key_name":"ss_discuss_days","max":0,"atri_keys":['ss_discuss_days']},
            {"key_name":"family",         "max":0,"atri_keys":['家族世帯']},
            {"key_name":"family_diff",    "max":0,"atri_keys":['家族世帯_変動']},
            {"key_name":"sold_count",     "max":0,"atri_keys":['sold_count']},
            {"key_name":"sold_count_diff","max":0,"atri_keys":['sold_count_diff']},
            {"key_name":"sold_price",     "max":0,"atri_keys":['sold_price']},
            {"key_name":"land_price",     "max":0,"atri_keys":['land_price']},
            {"key_name":"kodate_rate",    "max":0,"atri_keys":['kodate_rate']},
            {"key_name":"buy_new_rate",   "max":0,"atri_keys":['buy_new_rate']},
        ];
        return max_sets;
    }

    scale_sales_max_sets(){
        let max_sets = [
            {"key_name" :"points", "max":0,
             "atri_keys":['s4_points','s9_points','s10_points']},
            {"key_name" :"total", "max":0,
             "atri_keys":['s4_total','s9_total','s10_total']},
            {"key_name" :"onsale", "max":0,
             "atri_keys":['s4_onsale','s9_onsale','s10_onsale']}
        ];
        return max_sets;
    }

    async load_near_city_profiles(pref,city,vue_obj){
        let req_url = this.server_api_base() +"NearCityProfiles/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city)+
            "?date=" + vue_obj.disp_date;
        
        let res = await fetch(req_url);
        let city_profiles = await res.json();
        
        let max_sets = this.near_city_profiles_max_sets();
        
        let city_profiles_tmp = [];
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
            
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( city_profile[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = city_profile[atri_key];
                }
            }
            city_profiles_tmp.push(city_profile);
        }
        
        city_profiles_tmp = city_profiles_tmp.sort(function(a, b) {
            return b["人口_25_59歳_万人"] - a["人口_25_59歳_万人"];
        });

        vue_obj.near_city_profiles = [];
        for( let city_profile of city_profiles_tmp ) {
            
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
                    
                    if (atri_key in ["持家率","戸建率"]){
                        continue
                    }
                    //数値の3桁区切り化
                    city_profile[atri_key] =
                        Number(city_profile[atri_key]).toLocaleString();
                }
            }
            
            vue_obj.near_city_profiles.push( city_profile );
        }
    }
    
    async load_city_ratings(pref,vue_obj){
        let req_url = this.server_api_base() +"CityRatings/"+
            encodeURIComponent(pref);
        
        let res = await fetch(req_url);
        let city_ratings = await res.json();
        
        let max_sets = this.ratings_max_sets();
        
        let city_ratings_tmp = [];
        for( let city_rating of city_ratings ) {
            city_rating = JSON.parse( city_rating );
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
		    if( isNaN( city_rating[atri_key] ) ){
			city_rating[atri_key] = 0;
		    }
                    if( city_rating[atri_key] > max_set.max ){
			max_set.max = city_rating[atri_key];
                    }
                }
            }
            city_ratings_tmp.push(city_rating);
        }

        city_ratings_tmp = city_ratings_tmp.sort(function(a, b) {
            return b["ss_sold_count"] - a["ss_sold_count"];
        });
        
        vue_obj.city_ratings = [];
        for( let city_rating of city_ratings_tmp ) {
            
            for( let max_set of max_sets ) {
                if ( max_set.max == 0 ){
                    continue
                }
                
                for( let atri_key of max_set.atri_keys ){
                    let graph_bar_key = atri_key + "_px";
                    city_rating[graph_bar_key] =
                        this.calc_graph_bar_px(city_rating[atri_key],
                                               0.0,
                                               max_set.max,
                                               50.0 );
                    //数値の3桁区切り化
                    city_rating[atri_key] =
                        Number(city_rating[atri_key]).toLocaleString();
                }
            }
            
            vue_obj.city_ratings.push( city_rating );
        }
    }
    
    async load_town_ratings(pref,city,vue_obj){
        let req_url = this.server_api_base() +"TownRatings/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
        
        let res = await fetch(req_url);
        let town_ratings = await res.json();
        
        let max_sets = this.ratings_max_sets();
        
        let town_ratings_tmp = [];
        for( let town_rating of town_ratings ) {
            town_rating = JSON.parse( town_rating );
            
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( isNaN( town_rating[atri_key] ) ){
                        town_rating[atri_key] = 0;
                    }
                    if( town_rating[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = town_rating[atri_key];
                }
            }
            town_ratings_tmp.push(town_rating);
        }
        town_ratings_tmp = town_ratings_tmp.sort(function(a, b) {
            return b["ss_sold_count"] - a["ss_sold_count"];
        });
        
        vue_obj.town_ratings = [];
        for( let town_rating of town_ratings_tmp ) {
            
            for( let max_set of max_sets ) {
                if ( max_set.max == 0 ){
                    continue
                }
                
                for( let atri_key of max_set.atri_keys ){
                    let graph_bar_key = atri_key + "_px";
                    
                    town_rating[graph_bar_key] =
                        this.calc_graph_bar_px(town_rating[atri_key],
                                               0,
                                               max_set.max,
                                               50 );
                    
                    //数値の3桁区切り化
                    town_rating[atri_key] =
                        Number(town_rating[atri_key]).toLocaleString();
                }
            }
            vue_obj.town_ratings.push( town_rating );
        }
    }
    
    town_profiles_max_sets(){
        let max_sets = [
            {"key_name" :"price", "max":0,
             "atri_keys":['price']},
            {"key_name" :"from_station", "max":0,
             "atri_keys":['from_station']},
            {"key_name" :"pop", "max":0,
             "atri_keys":[
                 'pop_2020_20_24','pop_2020_25_59','pop_2020_60']},
            {"key_name" :"pop_diff", "max":0,
             "atri_keys":[
                 'pop_diff_20_24','pop_diff_25_59','pop_diff_60']}
        ];
        return max_sets;
    }
    
    async load_town_profiles(pref,city,vue_obj){
        let req_url = this.server_api_base() +"TownProfiles/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city);
        
        let res = await fetch(req_url);
        let town_profiles = await res.json();

        let max_sets = this.town_profiles_max_sets();

        let town_profiles_tmp = [];
        for( let town_profile of town_profiles ) {
            town_profile = JSON.parse( town_profile );

            town_profile["price"] = Math.round(town_profile["price"] / 10000);
            town_profile["from_station"] =
                Math.round( town_profile["from_station"] / 100 ) / 10;
            
            //最大値算出
            for( let max_set of max_sets ) {
                for( let atri_key of max_set.atri_keys ){
                    if( town_profile[atri_key] <= max_set.max ){
                        continue
                    }
                    max_set.max = town_profile[atri_key];
                }
            }
            town_profiles_tmp.push(town_profile);
        }
        
        vue_obj.town_profiles = [];
        for( let town_profile of town_profiles_tmp ) {
            
            for( let max_set of max_sets ) {
                if ( max_set.max == 0 ){
                    continue
                }
                
                for( let atri_key of max_set.atri_keys ){
                    let graph_bar_key = atri_key + "_px";
                    
                    town_profile[graph_bar_key] =
                        this.calc_graph_bar_px(town_profile[atri_key],
                                               0,
                                               max_set.max,
                                               50 );
                    //数値の3桁区切り化
                    town_profile[atri_key] =
                        Number( town_profile[atri_key] ).toLocaleString();
                }
            }
            vue_obj.town_profiles.push( town_profile );
        }

        vue_obj.town_profiles = this.sort_tbl(vue_obj.town_profiles, "price", 1);
    }
    
    async load_city_profile(pref,city,vue_obj){
        let req_url = this.server_api_base() +"CityProfile/"+
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
            city_profile["入手_分譲"] +
            city_profile["入手_新築"] +
            city_profile["入手_建替"];
        
        city_profile["入手_分譲"] =
            Math.round(city_profile["入手_分譲"] / tmp_sum *100);
        city_profile["入手_新築"] =
            Math.round(city_profile["入手_新築"] / tmp_sum *100);
        city_profile["入手_建替"] =
            Math.round(city_profile["入手_建替"] / tmp_sum *100);
        
        let atri_keys =
            ["人口_20_24歳_万人","人口_25_59歳_万人","人口_60歳_万人",
             "総世帯","家族世帯","単身世帯"]
        for( let atri_key of atri_keys ) {
            for ( let diff_key of ["_差","_変動"] ) {

                city_profile[atri_key+diff_key] =
                    city_profile[atri_key] - city_profile[atri_key+"_2015"];
                
                city_profile[atri_key+diff_key] =
                    Math.round(city_profile[atri_key+diff_key]*100) /100;

                city_profile[atri_key+diff_key] =
                    city_profile[atri_key+diff_key].toLocaleString();
                if(! city_profile[atri_key+diff_key]){
                    city_profile[atri_key+diff_key] = "±0"
                } else if (city_profile[atri_key+diff_key].indexOf("-") < 0 ){
                    city_profile[atri_key+diff_key] =
                        "+"+ city_profile[atri_key+diff_key];
                }
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
            city_profile["citycode"].substr( 0,city_profile["citycode"].length-1);

        vue_obj.city_profile = city_profile;
    }
    
    async load_near_city_data(pref,city,vue_obj){
        let req_url = this.server_api_base() +"SalesCountByNearCity/"+
            encodeURIComponent(pref) +"_"+ encodeURIComponent(city)+
            "?date=" + vue_obj.disp_date;
        
        let res = await fetch(req_url);
        let city_sales = await res.json();
        city_sales = this.conv_counts_for_disp( city_sales );
        vue_obj.near_city_sales = city_sales;
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
    
    conv_counts_for_disp( sales_counts ){
        // 最大/最小値を算出する為の準備
        let atri_sets = {}
        const atri_keys = ["onsale_count", "onsale_price",  "onsale_days",
                           "discuss_count","discuss_price", "discuss_days",
                           "sold_count",   "sold_price" ]
        
        for( let atri_key of atri_keys ) {
            atri_sets[atri_key] = new Set();
        }
        
        for( let sales_count of sales_counts ) {
            // 円→百万円
            for( let atri_key of ["discuss_price","onsale_price","sold_price"] ) {
                sales_count[atri_key] =
                    Math.round(sales_count[atri_key] /1000000)
            }
            
            for( let atri_key of atri_keys ) {
                atri_sets[atri_key].add( sales_count[atri_key] );
            }
        }
        
        // sort
        sales_counts = sales_counts.sort(function(a, b) {
            return b["onsale_count"] - a["onsale_count"];
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
    
    conv_price_counts_for_disp( sales_counts ){
        // 最大/最小値を算出する為の準備
        let atri_sets = {}
        const atri_keys = ["onsale_count", "onsale_days",
                           "discuss_count","discuss_days",
                           "sold_count",   "sold_count_q"  ]
        
        for( let atri_key of atri_keys ) {
            atri_sets[atri_key] = new Set();
        }
        
        for( let sales_count of sales_counts ) {
            for( let atri_key of atri_keys ) {
                atri_sets[atri_key].add( sales_count[atri_key] );
            }
        }
        
        // sort
        sales_counts = sales_counts.sort(function(a, b) {
            return b["onsale_count"] - a["onsale_count"];
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
    
    conv_scale_counts_for_disp( sales_counts ){
        // 最大/最小値を算出する為の準備
        let atri_sets = {}
        const atri_keys = ["s4_points",  "s9_points",  "s10_points",
                           "s4_total",   "s9_total",   "s10_total",
                           "s4_onsale",  "s9_onsale",  "s10_onsale"]
        
        for( let atri_key of atri_keys ) {
            atri_sets[atri_key] = new Set();
        }
        
        for( let sales_count of sales_counts ) {
            for( let atri_key of atri_keys ) {
                atri_sets[atri_key].add( sales_count[atri_key] );
            }
        }
        
        // sort
        sales_counts = sales_counts.sort(function(a, b) {
            return b["s10_points"] - a["s10_points"];
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
