import {login, register_user} from '@/api'
import {EventBus} from '../../main'
export default {
    namespaced: true,

    state: () => ({
        user: {},
        jwt: ''
    }),

    getters: {
        user: (state) => state.user,

        jwtToken: (state) => state.jwt,

        isAuthenticated(state){
            if (!state.jwt || state.jwt.split('.').length < 3) {return false}
            const data = JSON.parse(atob(state.jwt.split('.')[1]))
            const exp = new Date(data.exp * 1000) // milliseconds
            const now = new Date()
            return (now < exp)
        }
    },

    mutations:{
        setUserData(state, user){
            state.user = user
        }, 
        setJwtToken(state, jwt){
            state.jwt = jwt
        }
        
    },
    
    actions: {
        loginToDB({commit}, form){
            return login(form)
                .then(response => {
                    if (response.status === 200){
                        commit('setUserData', response.data.user)
                        commit('setJwtToken', response.data.jwt)
                    }
                })
                .catch(error => {
                    if (error.response.status === 401){
                        EventBus.$emit('failedLogin', 'La contraseña es incorrecta. Por favor, inténtalo de nuevo.')
                    }
                    else if (error.response.status === 404){
                        EventBus.$emit('failedLogin', 'El usuario o email no existen. Por favor, inténtalo de nuevo.')
                    }
                    else{
                        EventBus.$emit('failedLogin', 'Ha ocurrido un error desconocido. Por favor inténtalo más tarde.')
                    }
                })

        },

        logout({commit}){
            commit('setJwtToken', '')
            commit('setUserData', {})
        },

        registerToDB({commit}, form){
            return register_user(form)
                .then(response => {
                    if (response.status === 200){
                        commit('setUserData', response.data.user)
                        commit('setJwtToken', response.data.jwt)
                    } 
                })
                .catch(error => {
                    if (error.response.status === 409){
                        EventBus.$emit('failedSignUp', 'El usuario ya existe. Por favor, inténtalo de nuevo con otro nombre de usuario / email.')
                    }
                })

        }
    }
}