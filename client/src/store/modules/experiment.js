import {postDatasetForExperiment, postExperimentToDB, postDatasetToDB, getExperimentExample} from '@/api'
import EventBus from '@/main'
import cloneDeep from 'lodash/cloneDeep'
export default {
    namespaced: true,

    state: () => ({
        experiment: {'category': null,
                     'creation_date': null,
                     'description': '',
                     'communities': null,
                     'dataset_id': null,
                     'dataset_name': null,
                     'experiment_id': null,
                     'experiment_name': null,
                     'metrics': null,
                     'network_json': null,
                     'thumbnail': null,
                     'visualization_params': null,
                     'user_id' : null
                    },
        isNewExperiment: true
      }),

      getters:{
        getExperiment: (state) => {return state.experiment},

        network: (state) => cloneDeep(state.experiment.network_json),

        getIsNewExperiment: (state) => state.isNewExperiment,

        getVisualizationParams: (state) => cloneDeep(state.experiment.visualization_params)
      },
    
      mutations: {
        setExperiment(state, experiment){
            state.experiment = experiment
        },
        setNetwork(state, network){
            state.experiment.network_json = network
        },
        setVisualizationParams(state, visualizationParams){
            state.visualization_params = visualizationParams
        },
        setExperimentName(state, experiment_name){
            state.experiment.experiment_name = experiment_name
        },
        setExperimentDescription(state, description){
            state.experiment.description = description
        },
        setThumbnail(state, thumbnail){
            state.experiment.thumbnail = thumbnail
        },
        setIsNewExperiment(state, isNewExperiment){
            state.isNewExperiment = isNewExperiment
        },

      },

      actions: {

        async getExperimentWithDataset({commit}, payload){
            const response = await postDatasetForExperiment(payload.method, payload.formData).catch( () => {
                EventBus.$emit('csvFormatError', 'El formato del archivo .csv es incorrecto. Por favor inténtalo con un formato distinto.')
            })
            commit('setExperiment', response.data)
            commit('setIsNewExperiment', true)
            commit('setVisualizationParams', response.data['visualizationParams'])
        },

        async saveExperiment({state, commit, rootState}){
            commit('setIsNewExperiment', false)
            const response = await postExperimentToDB(state.experiment, rootState.auth.jwt)
            commit('setExperiment', response.data.experiment)      
        },

        postDataset({commit, rootState}, payload){
            commit('setIsNewExperiment', true)
            return postDatasetToDB(payload.formData, rootState.auth.jwt)
        },

        async getExperimentExample({commit}){
            const response = await getExperimentExample()
            commit('setExperiment', response.data)
            commit('setIsNewExperiment', true)
            commit('setVisualizationParams', response.data['visualizationParams'])
        }

    }
}