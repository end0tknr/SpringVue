'use strict';
{
    var WindowBase = function() {};

    WindowBase.prototype = {
        
        init_window: function(){
            // 外部htmlを include
            this.load_html(".header_container",     "index_header.html");
            this.load_html(".page_top_container",   "index_carousel_large.html" );
            this.load_html(".page_middle_container","index_carousel_small.html" );
            this.load_html(".page_middle_container","index_carousel_medium.html");
            this.load_html(".column_left",          "index_bottom_left.html"    );
            this.load_html(".column_center",        "index_bottom_center.html"  );
            this.load_html(".column_right",         "index_bottom_right.html"   );

            var this_obj = this;
            this.sleep(2, function(){ this_obj.init_window_sub()} );
        },

        init_window_sub:function(){
            this.init_sp_menu();
            
            var tab_menus = document.querySelectorAll('.tab_menu');
            tab_menus.forEach(tab_menu=>{
                this.init_tab_menu( tab_menu );
            });
            
            var carousels = document.querySelectorAll('.carousel');
            carousels.forEach(carousel=>{
                this.init_carousel( carousel );
                this.update_carousel_buttons( carousel );
            });
            
            // カルーセルのサイズをwinサイズに追従
            window.addEventListener('resize', () => {
                carousels.forEach(carousel=>{
                    this.slide_carousel( carousel );
                });
            });
            
            document.querySelectorAll('.copyright_year').forEach(span=>{
                span.innerHTML = new Date().getFullYear();
            });
        },

        init_sp_menu: function(){
            var pc_menu_ul = document.querySelector('#pc_menu nav ul');
            var sp_menu_ul = pc_menu_ul.cloneNode(true);

            var sp_menu_nav = document.querySelector('#sp_menu_overlay nav');
            sp_menu_nav.after(sp_menu_ul);

            this.sp_menu_open   = document.getElementById('sp_menu_open');
            this.sp_menu_close  = document.getElementById('sp_menu_close');
            this.sp_menu_overlay= document.getElementById('sp_menu_overlay');

            this.sp_menu_open.addEventListener('click', () => {
                this.sp_menu_overlay.classList.add('show');
                this.sp_menu_open.classList.add('hide');
            });
            this.sp_menu_close.addEventListener('click', () => {
                this.sp_menu_overlay.classList.remove('show');
                this.sp_menu_open.classList.remove('hide');
            });
            
        },

        init_carousel: function(carousel){
            carousel.current_index = 0;
            carousel.prev_button = carousel.querySelector('.carousel_prev');
            carousel.next_button = carousel.querySelector('.carousel_next');
            carousel.ul     = carousel.querySelector('ul');
            carousel.slides = carousel.querySelectorAll('ul li');
            
            // ボタンによる左右スライド
            carousel.prev_button.addEventListener('click', () => {
                carousel.current_index -= 1;
                this.update_carousel_buttons(carousel);
                this.slide_carousel(carousel);
            });
            carousel.next_button.addEventListener('click', () => {
                carousel.current_index += 1;
                this.update_carousel_buttons(carousel);
                this.slide_carousel(carousel);
            });

        },
        
        init_tab_menu: function(tab_menu){
            var this_obj = this;

            var tab_menu_items    = tab_menu.querySelectorAll('ul li');
            var tab_menu_contents = tab_menu.querySelectorAll('section');

            for (let i = 0; i < tab_menu_items.length; i++) {
                tab_menu_items[i].addEventListener('click', event => {
                    event.preventDefault();
                    
                    tab_menu_items.forEach(item => {
                        item.classList.remove('active');
                    });
                    tab_menu_items[i].classList.add('active');
                    
                    tab_menu_contents.forEach(content => {
                        content.classList.remove('active');
                    });
                    tab_menu_contents[i].classList.add('active');
                });
            }
        },

        update_carousel_buttons: function (carousel) {
            carousel.prev_button.classList.remove('hidden');
            carousel.next_button.classList.remove('hidden');
        
            if (carousel.current_index == 0) {
                carousel.prev_button.classList.add('hidden');
                
            }
            if (carousel.current_index === carousel.slides.length - 1) {
                carousel.next_button.classList.add('hidden');
            }
        },

        slide_carousel: function(carousel) {
            var slide_w = carousel.slides[0].getBoundingClientRect().width;
            var current_index = carousel.current_index;
            
            carousel.ul.style.transform =
                `translateX(${-1 * slide_w * current_index}px)`;
        },

        // jquery.loca()の大体
        load_html: function(selector, url){
            var xhr = new XMLHttpRequest();
            xhr.responseType="document";
            xhr.open("get", url, true);

            xhr.onreadystatechange = function(){
                if(xhr.readyState === 4 && xhr.status === 200) {
                    document.querySelectorAll(selector).forEach(elm=>{
                        
                        var new_elms =
                            xhr.responseXML
                            .getElementsByTagName("body")[0].childNodes;
                        
                        for (var i=0; i<new_elms.length; i++ ) {
                            elm.appendChild( new_elms.item(i) );
                        }
                    });
                }
            };
            xhr.send();
        },

        // refer from https://www.sejuku.net/blog/24629
        sleep: function (waitSec,callbackFunc) {
            var spanedSec = 0;
            
            var id = setInterval(function () {
                spanedSec++;
                if (spanedSec >= waitSec) {
                    if (callbackFunc) callbackFunc();
                    clearInterval(id);
                }
            }, 1000);
        }
    };

    var win_base = new WindowBase();
    win_base.init_window();
}
