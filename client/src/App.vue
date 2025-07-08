<template>
  <div id="app" class="custom-scrollbar">
    <b-navbar toggleable="md" type="dark" variant="dark" id="nav-bar">
      <b-navbar-brand id="brand" to="/">network.ly</b-navbar-brand>
      <b-navbar-toggle target="routes"></b-navbar-toggle>
      <b-collapse is-nav id="routes">
        <b-navbar-nav class="mr-auto">
          <b-nav-item left to="/graph-visualization"> Visualizar grafo </b-nav-item>
          <b-nav-item-dropdown left text="Detección de comunidades" ref="dropdown">
            <b-dropdown-item to="/community-detection/louvain"
              >Método de Louvain</b-dropdown-item
            >
            <b-dropdown-item to="/community-detection/girvan-newman"
              >Método de Girvan-Newman</b-dropdown-item
            >
          </b-nav-item-dropdown>

          <b-nav-item left v-if="isAuthenticated" to="/user-datasets"> Datasets </b-nav-item>
          <b-nav-item left v-if="isAuthenticated" to="/user-experiments"> Experimentos </b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item right to="/about"> About </b-nav-item>
          <b-nav-item v-if="!isAuthenticated" right to="/user-signup"> Registrarse </b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav>
          <b-nav-item-dropdown right text="Perfil">
            <!-- Profile icon -->
            <template v-slot:button-content>
              <b-avatar icon="person" scale="0.5"></b-avatar>
            </template>

            <b-dropdown-item v-if="!isAuthenticated" @click=toUserSignUp()> 
              <b-icon icon="person-plus" aria-hidden="true" scale="0.9" class="pt-1 ml-1"></b-icon>
              <span class="mr-1"> Registrarse </span>
            </b-dropdown-item>

            <b-dropdown-item v-if="!isAuthenticated" @click=showLoginModal()> 
              <b-icon icon="box-arrow-in-right" aria-hidden="true" scale="0.9" class="pt-1 mr-1"></b-icon>
              <span class="mr-1"> Iniciar sesión </span>
            </b-dropdown-item>
            <b-dropdown-item v-else @click=logout() right> 
              <b-icon icon="box-arrow-right" aria-hidden="true" scale="0.9" class="pt-1"></b-icon>
              <span class="mr-1"> Cerrar sesión </span>
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
        
      </b-collapse>
    </b-navbar>

    <router-view/>
    <UserLoginModal :showModal="this.showModal" @hideLoginModal="hideLoginModal"/>

    <div id="login-success">
      <b-alert :show="dismissCountDown" dismissible fade variant="success" @dismissed="dismissCountDown=0"
        @dismiss-count-down="countDownChanged">
        Has iniciado sesión correctamente. 
      </b-alert>
    </div>

  </div>
</template>


<script>
import UserLoginModal from '@/components/UserLoginModal.vue';
import {EventBus} from './main'

export default {  
  components: { UserLoginModal },
  data() {
    return {
      showModal: false
    }
  },
  computed: {
      isAuthenticated() {
          return this.$store.getters['auth/isAuthenticated'];
      }
  },
  methods: {
      /// Modal
      showLoginModal() {
          this.showModal = true;
      },
      hideLoginModal(showModal) {
          this.title = '';
          this.showModal = showModal;
      },
      async logout(){
        await this.$store.dispatch('auth/logout')
        this.$router.push('/')        
        this.toast_on_logout()
      },
      toast_on_logout(){
        this.$bvToast.toast('Esperamos verte pronto!', {
        title: `Has cerrado sesión.`,
        variant: 'info',
        solid: true
        })
      },
      toUserSignUp(){
        this.$router.push('/user-signup')
      }
  },
  mounted() {
    EventBus.$on('failedAuthentication', (msg) => {
      this.errorMsg = msg
    })
    
  }
};
</script>


<style lang="scss">
@import "./assets/scss/custom.scss";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #046865;
    }
  }
}

#brand {
  color: #fcfff7;
}

#nav-bar {
  box-shadow: rgba(0, 0, 0, 0.1) 0px 10px 15px -3px,
    rgba(0, 0, 0, 0.05) 0px 4px 6px -2px;
}

.fade-enter {
  opacity: 0;
}

.fade-enter-active {
  transition: opacity 0.1s ease;
}

.fade-leave-active {
  transition: opacity 0.1s ease;
  opacity: 0;
}

// body {
//   overflow-y: hidden;
// }

.custom-scrollbar {
  /* Set the desired width for the scrollbar */
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1; /* thumb color, track color */

  /* For WebKit-based browsers */
  &::-webkit-scrollbar {
    width: 10px;
  }
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
  }
  &::-webkit-scrollbar-thumb {
    background: #888;
  }
  &::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
}
</style>
