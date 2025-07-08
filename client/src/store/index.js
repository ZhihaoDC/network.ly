import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersist from 'vuex-persist';
import authentication from '@/store/modules/authentication'
import experiment from '@/store/modules/experiment'
// import {getExperiments, deleteExperiment, postDataset, deleteDataset} from '@/api'

Vue.use(Vuex)

const vuexLocalStorage = new VuexPersist({
    key: 'vuex',
    storage: window.sessionStorage
})


export default new Vuex.Store({
    modules: {
        auth: authentication,
        experiment: experiment
    },
    plugins: [vuexLocalStorage.plugin]
})