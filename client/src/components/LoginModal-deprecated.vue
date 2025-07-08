<template>
    
    <!-- <b-container fluid="md"> -->
    <b-modal v-model="showModal" ok-only @hide="resetInfoModal" @show="printShow" @change="changed" no-stacking id="loginModal">
    <b-form>
        <b-form-group label="Email" label-for="email">
            <b-form-input
            id="email"
            v-model="form.identification"
            placeholder="Introduce tu nombre de usuario o email"
            :state="is_identification_valid"
            lazy-formatter
            :formatter="identification_format"
            required
            ></b-form-input>
            <b-form-invalid-feedback id="input-live-feedback">
                El nombre de usuario o email es incorrecto o no existen.
            </b-form-invalid-feedback>
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
        <p v-if="errorMessage">{{errorMessage}}</p>
        <b-button block type="submit" @click.stop.prevent="login" variant="primary"
        class="content-item submit-button">
            Iniciar sesión
        </b-button>
        

    </b-form>
    
<!-- </b-container> -->
    </b-modal>
    
</template>

<script>
import {EventBus} from '../main'
export default{
    name: "LoginModal",
    props: ["showModal"],
    data: function(){
        return {
            title: 'Identifícate',
            identification : '',
            is_identification_valid: null,
            is_password_valid: null,
            form: {
                    username: '',
                    email: '',
                    password: '',
                },
            errorMessage: null
        }
    },
    methods: {
        async login(){
            this.errorMessage = ''
            await this.$store.dispatch('auth/loginToDB', this.form)
                .then(() => {
                    if (!this.errorMessage){
                        this.resetInfoModal()
                    }
                })
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
        },
        printShow(){
            console.log(this.showModal)
        },
        changed(){
            console.log("AAAAAAAAAAAAAAAAAAAA")
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