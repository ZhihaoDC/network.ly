<template>
    
    <!-- <b-container fluid="md"> -->
    <b-modal v-model="showModal" :title=title ok-only @hide="resetInfoModal" @change="changed" no-stacking>
    <b-form>
        <b-form-group label="Email" label-for="email">
            <b-form-input
            id="email"
            v-model="form.identification"
            placeholder="Introduce tu email"
            required
            ></b-form-input>
        </b-form-group>


        <b-form-group label="Contraseña:" label-for="password">
            <b-form-input
            v-model="form.password"
            type="password"
            placeholder="Introduce una contraseña"          
            :state="is_password_valid"
            lazy-formatter
            :formatter="password_format"
            required
            ></b-form-input>
            <b-form-invalid-feedback id="input-live-feedback">
                La contraseña es incorrecta.
            </b-form-invalid-feedback>
        </b-form-group>
        <p id="error-message" v-if="errorMessage">{{errorMessage}}</p>
        <b-button block type="submit" @click.stop.prevent="login" variant="primary"
        class="content-item submit-button">
            Iniciar sesión
        </b-button>
        <b-link to="/user-signup" @click=resetInfoModal()> ¿No tienes cuenta? Crea una cuenta </b-link>

    </b-form>
    
<!-- </b-container> -->
    </b-modal>
    
</template>

<script>
import {EventBus} from '../main'
export default{
    name: "UserLoginModal",
    props: ["showModal"],
    data: function(){
        return {
            title: 'Identifícate',
            identification : '',
            is_identification_valid: true,
            is_password_valid: null,
            form: {
                    identification: '',
                    password: '',
                },
            errorMessage: null
        }
    },
    methods: {
        async login(){
            this.errorMessage = ''
            await this.$store.dispatch('auth/loginToDB', this.form)
                .then((response) => {
                    console.log(response)

                    if (!this.errorMessage){
                        this.resetInfoModal()
                        this.toast_on_login()
                        this.$router.push('/home-user')
                    }
                })
                .catch(
                    console.log("AAAAA")
                )
        },

        identification_format(identification){
            const isValidEmail = String(identification)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                );
            if (isValidEmail) {this.form.email = identification}
            else {this.form.username = identification}
            return identification
        },

        resetInfoModal() {
            this.showModal = false;
            this.$emit('hideLoginModal', this.showModal)
            this.form = {
                    username: '',
                    email: '',
                    password: '',
                }
            this.errorMessage = ""
        },        
        toast_on_login(){
            let username = this.$store.getters['auth/user'].username
            this.$bvToast.toast('Te has identificado con éxito.', {
            title: `Bienvenid@, ${username}.`,
            variant: 'success',
            solid: true
            })
        }
    },

    mounted() {
        EventBus.$on('failedLogin', (errorMessage) =>{
            this.errorMessage = errorMessage
        })
    },
    beforeDestroy () {
        EventBus.$off('failedLogin')
    }
}
</script>
<style>
#error-message{
    color:red;
    font-size: small;
}   
</style>