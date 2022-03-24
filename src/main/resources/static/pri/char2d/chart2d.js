(function () {
    "use strict";
    
    let map = "";
    let markers = {};
    let marker_style = {icon: {fillOpacity: 0.8,
                               scale      : 15,
                               strokeColor: "#AAA",
                               strokeWeight: 1.0},
                        label:{color: '#FFF',
                               fontSize: '14px',
                               fontWeight: 'bold'} };
    let marker_colors = [["#C00000","#FFF",""],
                         ["#FF0000","#FFF",""],
                         ["#FFC000","#000",""],
                         ["#FFFF00","#000",""],
                         ["#00B050","#000",""],
                         ["#00B0F0","#000",""],
                         ["#0070C0","#FFF",""],
                         ["#002060","#FFF",""],
                         ["#7030A0","#FFF",""]];
    
    let vueapp = Vue.createApp({
        data(){
            return { gis_datas : [],
		     selected_gis_data : "",
                     col_desc_class : ["col_description"] }
        },
        mounted(){
            const script = document.createElement('script');
            script.src =
                'https://maps.googleapis.com/maps/api/js'+
                '?key='+app_conf.gmap_api_key;
            script.async = true;
            document.head.appendChild(script);

            let timer = setInterval(() => {
                if(! window.google){ return; }
                
                clearInterval(timer);

                var mapLatLng =
                    new google.maps.LatLng({lat: app_conf.map_default.lat,
                                            lng: app_conf.map_default.lng});
                map = new google.maps.Map(
                    document.getElementById('map'),
                    {center: mapLatLng,  zoom: 15} );
            }, 500);

        },
        methods : {
            set_marker_color(data_name){
                for( let marker_color of marker_colors ){
                    if (marker_color[2]){
                        continue;
                    }
                    marker_color[2] = data_name;

                    for (let gis_data of this.gis_datas ){
                        if (data_name != gis_data.data_name ){
                            continue;
                        }
                        gis_data.color = marker_color[0];
                    }
                    return marker_color;
                }
                return;
            },

            toggle_col_desc(){
                if (this.col_desc_class.indexOf("full") >= 0 ){
                    this.col_desc_class = ["col_description"]
                } else {
                    this.col_desc_class.push("full")
                }
            },
            async get_gis_datanames(){
                let data_names = [];
                try {
                    let axios_res = await axios.get(
                        app_conf.api_base_url+'/api/gis/datanames');
                    data_names = axios_res.data;
                } catch (error){
                    console.log("ERROR", error);
                    return;
                }

                for( let data_name of data_names ){
                    let col_defs  = [];
                    try {
                        let req_url = app_conf.api_base_url+'/api/gis/coldefs/'
                            + data_name["data_name"];
                        
                        let axios_res = await axios.get(req_url);
                        
                        col_defs = axios_res.data;
                    } catch (error){
                        console.log("ERROR", error);
                        return;
                    }

                    let col_descs = [];
                    for( let col_name in col_defs ){
                        col_descs.push( col_defs[col_name] );
                    }

                    data_name["columns"] = col_descs.sort().join(" ");
                    data_name["kbyte"] =
                        Number(data_name["kbyte"]).toLocaleString();
                    this.gis_datas.push(data_name);
                }

                this.selected_gis_data = data_names[0].data_name;
            },
            clear_gis_data(){
                for (let data_name in markers ){
                    for (let i in markers[data_name] ){
                        markers[data_name][i].setMap(null);
                        markers[data_name][i] = null;
                    }
                }
                markers = {};
            },
            async find_gis_data(){
                let data_name = this.selected_gis_data;
                
                let latlngBounds = map.getBounds();
                let neLatlng = latlngBounds.getNorthEast();
                let swLatlng = latlngBounds.getSouthWest();
                let coord = [neLatlng.lat(),
                             neLatlng.lng(),
                             swLatlng.lat(),
                             swLatlng.lng()];
                let req_url =
                    app_conf.api_base_url+'/api/gis/find/' + data_name +
                    "?co="+coord.join(",");
                let gis_datas = [];
                try {
                    let axios_res = await axios.get(req_url);
                    gis_datas = axios_res.data;
                } catch (error){
                    console.log("ERROR", error);
                    return;
                }

                let marker_color = this.set_marker_color(data_name);
                if (! marker_color){
                    return;
                }

                let i = 0;
                for(let gis_data of gis_datas){
                    i += 1;
                    let marker = this.make_map_marker(gis_data, marker_color, i);

                    if( data_name in markers == false) {
                        markers[data_name] = [];
                    }
                    markers[data_name].push(marker);
                }
            },
            
            make_map_marker( gis_data, marker_color,i){
                let marker_latlng =
                    new google.maps.LatLng({lat: gis_data.geom[1],
                                            lng: gis_data.geom[0]});
                let marker_icon = marker_style.icon;
                marker_icon.fillColor = marker_color[0];
                marker_icon.path= google.maps.SymbolPath.CIRCLE;
                let marker_label= marker_style.label;
                marker_label.text = (i+1).toString();
                marker_label.color= marker_color[1];
                
                let marker = new google.maps.Marker({
                    position: marker_latlng,
                    map  : map,
                    icon : marker_icon,
                    label: marker_label });
                
                let infoWindow = new google.maps.InfoWindow({
                    content: gis_data["公示価格"].toLocaleString()
                    //content: gis_data["調査価格"].toLocaleString()
                });
                
                marker.addListener('click',function() {
                    infoWindow.open(map, marker);
                });

                return marker;
            },
        }
    })
    
    class Chart2d {
        constructor() {
            this.vueapp   = vueapp;
        }
        
        init_page=()=> {
            this.vueapp.mount('#vueapp');
        }
        
    }

    window.char2d = new Chart2d();
    char2d.init_page();

}());
