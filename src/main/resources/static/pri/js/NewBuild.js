'use strict';
class NewBuild extends AppBase {
    constructor() {
        super(); // 仕様上 thisを使う前にsuper()を呼ぶ要あり
    }
    
    init_window =async()=> {
        this.init_jpn_map_modal();
	
        let pref = this.get_cookie("pref") || "東京都";
        this.load_pref_info(pref);
    }

    load_pref_info=(pref)=> {
        document.getElementById('pref_name').textContent = pref;
    }

    init_jpn_map_modal=()=> {
        const close = document.getElementById('close_jpn_map_modal' );
        const modal = document.getElementById('jpn_map_modal');
        const mask  = document.getElementById('mask');
        
        // document.getElementById('open_jpn_map_modal').addEventListener(
        //     'click', () => {
        //         modal.classList.remove('hidden');
        //         mask.classList.remove('hidden');
        //     });
        
        close.addEventListener('click', () => {
            modal.classList.add('hidden');
            mask.classList.add('hidden');
        });
        
        mask.addEventListener('click', () => {
            close.click();
        });

        let pref_divs = document.querySelectorAll("#japan-map div div.area div");
        pref_divs.forEach((div_elm)=>{
            div_elm.addEventListener('click', () => {
                this.set_pref( div_elm.textContent );
            });
        });
        
    }

    set_pref=(pref)=>{
        if ( pref =="東京"){
            pref += "都"
        } else if( pref=="北海道"){

        } else if( pref=="京都" || pref=="大阪"){
            pref += "府"
        } else {
            pref += "県"
        }
        this.set_cookie("pref",pref,
                        {expires:new Date(Date.now()+86400e3*60) } );
	this.load_pref_info(pref);
        document.getElementById('close_jpn_map_modal').click();
    }
}

let new_build = new NewBuild();
new_build.init_window();
