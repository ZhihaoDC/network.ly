import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import './assets/css/main.css';



Vue.config.productionTip = false

export var store = {
  state: {
    lastComputedExperiment: Object,
    isNewExperiment: true
  },
  getLastComputedExperiment(){
    return this.state.lastComputedExperiment
  },
  setLastComputedExperiment(lastComputedExperiment){
    this.state.lastComputedExperiment = lastComputedExperiment
  },
  setIsNewExperiment(isNewExperiment){
    this.state.isNewExperiment = isNewExperiment
  },
  getExperimentJSON(){
    return this.state.lastComputedExperiment.network_json
  },
  setExperimentJSON(new_json){
    this.state.lastComputedExperiment.network_json = new_json
  },
  getExperimentThumbnail(){
    return this.state.lastComputedExperiment.thumbnail
  },
  setExperimentThumbail(new_thumbnail){
    this.state.lastComputedExperiment.thumbnail = new_thumbnail
  }
}


new Vue({
  router,
  data(){
    return{
      sharedState: store.state
    }
  }
  ,
  render: h => h(App)
}).$mount('#app')
