'use strict';
class NewBuild extends AppBase {
    constructor() {
        super(); // 仕様上 thisを使う前にsuper()を呼ぶ要あり
    }
    
    init_window =async()=> {
    }
}

let new_build = new NewBuild();
new_build.init_window();
