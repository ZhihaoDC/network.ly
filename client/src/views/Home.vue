<template>
    
  
  <b-container fluid class="custom-container p-auto">
    <b-row>
      <b-col md-12>
        <h1 id="header">Bienvenido a network.ly</h1>
        <h4>
          Herramienta de detección de comunidades y visualización de grafos.
        </h4>
        <br />
        <!-- <h5>La detección de comunidades agrupa los nodos en comunidades en función de las relaciones entre sus individuos, 
          lo cual descubre propiedades que no son visibles a simple vista.
          
          Se diferencia del clustering tradicional de grafos en que no utiliza las propiedades de cada inviduo.
        </h5> -->

        <h5>
          Agrupa las redes por los atributos que lo relacionan. Representa redes
          y edítalas a tu gusto. También puedes almacenar todos los resultados.
        </h5>
        <router-link to="/about" id="about-link">Aprende más sobre la detección de comunidades</router-link>
        <br />

        <b-row v-if="!example_submitted" class="mt-4">
          <b-button @click=showExample() size="lg" class="ml-auto" variant="primary">
            ¡Pruébame!
          </b-button>

          <b-button @click=showLoginModal() size="lg" class="mr-auto ml-4" variant="outline-primary">
            Identifícate
          </b-button>
          <UserLoginModal :showModal="this.showModal" @hideLoginModal="hideLoginModal"/>
        </b-row>
        <b-row v-else class="mt-4 justify-content-center">
          <b-spinner
            variant="primary"
            label="Spinning"
            size="lg"
            id="spinner"
          ></b-spinner>
        </b-row>
      </b-col>
    </b-row>

    <b-row>
      <b-col md-12>
        <div class="tools">
          <b-card-group deck>
            <a href="/community-detection">
              <b-card title="Detectar comunidades" img-src="../assets/static/webp/network-community.webp" alt="Community Detection" size="sm" class="mb-4" img-height="300" img-width="100"
                id="b-card">
                <b-card-text>
                  Clusterizar un grafo y representarlo.
                </b-card-text>
              </b-card>
            </a>

            <a href="/graph-visualization">
              <b-card title="Visualizar grafo" img-src="../assets/static/webp/network-visualization.webp" alt="Visualize network" size="sm" class="mb-6" img-height="300" img-width="300"
                id="b-card">
                <b-card-text>
                  Representar un grafo, cambiar los nodos de color y posición.
                </b-card-text>
              </b-card>
            </a>


            <a href="/user-datasets">
              <b-card v-if="isAuthenticated" title="Mis Datasets" img-src="../assets/static/webp/datasets.webp" alt="Datasets" class="mb-6" img-height="300" img-width="300"
                id="b-card">
                <b-card-text>
                  Subir y gestionar datasets. Iniciar un experimento con un dataset existente.
                </b-card-text>
              </b-card>
            </a>

            <a href="/user-experiments">
              <b-card v-if="isAuthenticated" title="Mis Experimentos" img-src="../assets/static/webp/laboratory.webp" alt="Experiments" size="sm" class="mb-4" img-height="300" img-width="100"
                id="b-card">
                <b-card-text>
                  Gestiona y visualiza de nuevo los experimentos que has creado.
                </b-card-text>
              </b-card>
            </a>
          </b-card-group>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import UserLoginModal from '@/components/UserLoginModal.vue';
export default {
  name: "Home",
  components: { UserLoginModal },
  data() {
    return {
      showModal: false,
      example_submitted: false
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
      read_file(file){
        return new Promise((resolve, reject) => {
          var reader = new FileReader()
          reader.readAsText(file)
          reader.onload = () => resolve(reader.result)
          reader.onerror = () => reject
        })
      },
      async showExample(){
          this.example_submitted = true
          await this.$store.dispatch("experiment/getExperimentExample")
          this.$router.push('/community-detection/louvain/experiment'); 
      },
      async logout(){
        await this.$store.dispatch('auth/logout')
        this.$router.push('/')
      },
      fetch_csv(file){            
        var rawFile = new XMLHttpRequest();
        rawFile.open("GET", file, false);
        rawFile.onreadystatechange = function (){
            if(rawFile.readyState === 4){
                if(rawFile.status === 200 || rawFile.status == 0){ console.log("SUCCESSSSS!!!") }
            }
        rawFile.send(null);
        }
      }
    }
};
</script>

<style scoped>
a:link {
  text-decoration: none;
}

a:visited {
  text-decoration: none;
}

a:hover {
  text-decoration: none;
}

a:active {
  text-decoration: none;
}

#start-button {
  padding: 0.5em 0.7em;
}

#about-link {
  color: #42b983;
  text-decoration: none;
}

#section-header {
  padding-top: 2rem;
  padding-bottom: 1rem;
}

#b-card {
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px,
    rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
  max-width: 20rem;
  min-width: 20rem;
  min-height: 30rem;
  min-height: 30rem;
}

#go {
  box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
}

.try-me {
  display: inline-block;
  color: aliceblue;
  background: #9363dc;
  border-radius: 10px;
  border-color: none;
  padding: 0.7em 1em;
  margin-bottom: 0.2em;
  cursor: pointer;
  box-shadow: rgba(57, 40, 58, 0.12) 0px 1px 3px,
    rgba(50, 40, 55, 0.24) 0px 1px 2px;
}

.try-me:hover {
  background-color: aliceblue;
  color: #050517;
  text-decoration: none;
}

.login {
  display: inline-block;
  color: aliceblue;
  background: #5bcaca;
  border-radius: 10px;
  border-color: none;
  padding: 0.7em 1em;
  margin-bottom: 0.2em;
  cursor: pointer;
  box-shadow: rgba(212, 233, 243, 0.979) 0px 1px 3px,
    rgba(176, 243, 255, 0.886) 0px 1px 2px;
}

.login:hover {
  background-color: #050517;
  color: aliceblue;
  text-decoration: none;
}

</style>