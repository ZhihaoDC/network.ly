<template>
    <b-container fluid="md" style="max-width: 40rem;" >
      <!-- <h2 id="header">Crear una cuenta nueva</h2> -->
      <h1 id="header">Regístrate {{ username }}</h1>
        <h4>
          Podrás guardar tus experimentos y datasets
        </h4>
        <br />
    <b-card class="signup-form my-auto">
      <b-form align="left">
        <div class="mx-auto" align="center"> <h5> Crear una cuenta nueva </h5></div>
        <b-form-group label-for="username" >
          <b-icon icon="person" aria-hidden="true" scale="1.5" class="pt-1 ml-1 mb-1"></b-icon>
          <b-form-input
            id="username"
            v-model="form.username"
            placeholder="Nombre de usuario (con este nombre te verán los demás)"
            :state="is_username_valid"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            {{username_invalid_msg}}
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label-for="email">
          <b-icon icon="envelope" aria-hidden="true" scale="1.5" class="pt-1 ml-1 mb-1"></b-icon>
          <b-form-input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Introduce tu email"
            :state="is_email_valid"
            lazy-formatter
            :formatter="email_format"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            {{email_invalid_msg}}
          </b-form-invalid-feedback>
        </b-form-group>
        
        <b-form-group label-for="password">
          <b-icon icon="lock" aria-hidden="true" scale="1.5" class="pt-1 ml-1 mb-1"></b-icon>
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
            La contraseña debe tener al menos 8 caracteres.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label-for="password-repeat">
          <b-icon icon="lock-fill" aria-hidden="true" scale="1.5" class="pt-1 ml-1 mb-1"></b-icon>
          <b-form-input
            v-model="form.password_confirmation"
            type="password"
            placeholder="Confirma la contraseña"
            :state="is_password_confirmation_valid"
            lazy-formatter
            :formatter="password_confirmation_format"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            Las contraseñas no coinciden
          </b-form-invalid-feedback>
        </b-form-group>

        <b-button block size="lg" type="submit" @click.stop.prevent="signUp" variant="primary" class="mt-4 mb-2 content-item submit-button"
          :disabled="!valid_fields">
          Registrarse
        </b-button>
      </b-form>
    </b-card>
  </b-container>
</template> 

<script>
// import UserLoginModal from "@/components/UserLoginModal.vue"
import {EventBus} from '../main'
export default {
    name: "UserSignUp",
    // components: UserLoginModal,
    data: function(){
        return{
            form: {
                    username: '',
                    email: '',
                    password: '',
                    password_confirmation: ''
                    },
            is_username_valid: null,
            is_email_valid: null,
            is_password_valid: null,
            is_password_confirmation_valid: null,
            email_invalid_msg: "El email debe contener una dirección de correo con '@'.",
            username_invalid_msg: "El email debe contener una dirección de correo con '@'."
        }
    },
    computed: {
      valid_fields(){
        return ((this.is_email_valid) & (this.is_password_valid) & (this.is_password_confirmation_valid))
      }
    },
    methods:{
      reset_error_msg(){
        this.email_invalid_msg = "El email debe contener una dirección de correo con '@'."
        this.errorMessage = null
      },
      email_format(email){      
        this.reset_error_msg()  
        const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        if (isValidEmail){
          this.is_email_valid = true
        }
        else{
          this.is_email_valid = false
        }
        return email
      },
      password_format(password){
        if (password.length == 0){
          this.is_password_valid = null
        }
        else if (password.length < 8){
          this.is_password_valid = false
        }
        else if (password.length >= 8 ){
          this.is_password_valid = true
        }
        return password

      },
      password_confirmation_format(password_confirmation) {
        let password = this.form.password
        if (password_confirmation.length === 0){
          this.is_password_confirmation_valid = null
        }
        else if (password_confirmation != password) {
          this.is_password_confirmation_valid = false
        } 
        else if (password_confirmation === password){
          this.is_password_confirmation_valid = true
        }   
        return password_confirmation
      },

      async signUp(){
        await this.$store.dispatch('auth/registerToDB', this.form)
        .then(() => {
          if (!this.errorMessage){
            this.$router.push('/')
          }
        })
        .catch(error => {
          console.log(error)
        })

      },
    },
    mounted() {
        EventBus.$on('failedSignUp', (errorMessage) =>{
            this.errorMessage = errorMessage
            this.is_email_valid = false
            this.is_username_valid = false
            this.username_invalid_msg = errorMessage
            this.email_invalid_msg = errorMessage
            console.log(errorMessage)
        })
    },
    beforeDestroy () {
        EventBus.$off('failedSignUp')
    }
}
</script>

<style scoped>
#signup-form{
  margin: 0 auto;
}
</style>