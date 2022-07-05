"use strict";
    
let vue_newbuild = Vue.createApp({
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
            sort_tbl_dirs : {
                "shop_sales"      : {},
                "shop_city_sales" : {},
                "city_sales"      : {},
                "price_sales"     : {},
                "town_sales"      : {},
                "town_profiles"   : {},
                "near_city_sales" : {},
                "near_city_profiles" : {} },
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
            newbuild.load_disp_date_range(this);
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
            this.load_town_profiles(this.pref_name,this.city_name);
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
        
        load_shops_data(pref){
            newbuild.load_shops_data(pref,this);
        },
        load_shop_city_data(pref,city){
            newbuild.load_shop_city_data(pref,city,this);
        },
        load_cities_data(pref,city){
            newbuild.load_cities_data(pref,city,this);
        },
        load_price_data(pref,city){
            newbuild.load_price_data(pref,city,this);
        },
        load_city_profile(pref,city){
            newbuild.load_city_profile(pref,city,this);
        },
        load_near_city_profiles(pref,city){
            newbuild.load_near_city_profiles(pref,city,this);
        },
        load_town_profiles(pref,city){
            newbuild.load_town_profiles(pref,city,this);
        },
        load_town_data(pref,city){
            newbuild.load_town_data(pref,city,this);
        },
        load_near_city_data(pref,city){
            newbuild.load_near_city_data(pref,city,this);
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
    
    async load_disp_date_range(vue_obj){
        let req_url = this.server_api_base() + "DispDateRange";

        let res = await fetch(req_url);
        let disp_dates = await res.json();
        vue_obj.disp_date_min = disp_dates[0];
        vue_obj.disp_date_max = disp_dates[1];
        vue_obj.disp_date     = disp_dates[1];

        vue_obj.load_shops_data(vue_obj.pref_name);
        vue_obj.load_cities_data(vue_obj.pref_name);
    }
    
    async load_shops_data(pref,vue_obj){
        let req_url = this.server_api_base() + "SalesCountByShop/"+
            encodeURIComponent(pref) + "?date=" + vue_obj.disp_date;

	
        let res = await fetch(req_url);
        let shop_sales = await res.json();
        shop_sales = this.conv_counts_for_disp( shop_sales );
        vue_obj.shop_sales = shop_sales;
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
        vue_obj.load_near_city_profiles(vue_obj.pref_name,vue_obj.city_name);
        vue_obj.load_town_profiles(vue_obj.pref_name,vue_obj.city_name);
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
        price_sales = this.conv_counts_for_disp( price_sales );
        vue_obj.price_sales = price_sales;
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
             "atri_keys":['年収_百万円']},
            {"key_name" :"setai_income", "max":0,
             "atri_keys":['世帯年収_100',       '世帯年収_100～200',
                          '世帯年収_200～300',  '世帯年収_300～400',
                          '世帯年収_400～500',  '世帯年収_500～700',
                          '世帯年収_700～1000', '世帯年収_1000～1500',
                          '世帯年収_1500']},
            {"key_name" :"old", "max":0,
             "atri_keys":[
                 '新築_世帯主_年齢_24',         '新築_世帯主_年齢_25_34',
                 '新築_世帯主_年齢_35_44',      '新築_世帯主_年齢_45_54',
                 '新築_世帯主_年齢_55_64',      '新築_世帯主_年齢_65']},
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
            return b["sold_count"] - a["sold_count"];
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

