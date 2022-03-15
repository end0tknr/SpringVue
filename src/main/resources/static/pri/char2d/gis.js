(function() {
    'use strict';

    axios.defaults.baseURL = 'http://localhost:8080';
    // axios.interceptors.request.use((config) => {
    // 	return config;
    // });
    // axios.interceptors.response.use((response) => {
    // 	return response;
    // });

    const gisChikaComponent = {
	props: ['id', 'email', 'password'],
	template: `
        <div>
            <div v-text="id"></div>
            <div v-text="email"></div>
            <div v-text="password"></div>
        </div>
    `
    };
    
    const app = Vue.createApp({
	data(){
            return { message: 'Demo Vue.js 3 + Axios',
		     gis_chikas : [] }
	},
	mounted(){
            axios.get('/api/char2d')
		.then((response)=>{
		    this.gischikas = response.data;
		})
		.catch((error)=>{
                    console.log(error)
                    console.log(JSON.stringify(error))
                    console.log(error.name)
                    console.log(error.message)
                    console.log(error.request)
                    console.log(error.response)
		})
		.finally(function(){
		})
	}
    })
    
    app.mount('#app');
})()

