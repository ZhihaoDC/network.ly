<template>
  <b-container fluid>
    <b-row>
      <b-col md-12>
        <h1 id="header">Bienvenido a network.ly, {{ user.username }}</h1>
        <h4>
          Herramienta de detección de comunidades y visualización de grafos.
        </h4>
        <br />
      </b-col>
    </b-row>
    <div class="tools">
      <b-row>
        <b-col md-12>
          <div class="tools">
            <b-card-group deck>
              
              <a href="/community-detection">
                <b-card title="Detectar comunidades" img-src="../assets/static/webp/network-community.webp"
                  alt="Community Detection" size="sm" class="mb-4" img-height="300" img-width="100" id="b-card">
                  <b-card-text>
                    Clusterizar un grafo y representarlo.
                  </b-card-text>
                </b-card>
              </a>

              <a href="/graph-visualization">
                <b-card title="Visualizar grafo" img-src="../assets/static/webp/network-visualization.webp"
                  alt="Visualize network" size="sm" class="mb-6" img-height="300" img-width="300" id="b-card">
                  <b-card-text>
                    Representar un grafo, cambiar los nodos de color y posición.
                  </b-card-text>
                </b-card>
              </a>

              <a href="/user-datasets">
                <b-card v-if="isAuthenticated" title="Mis Datasets" img-src="../assets/static/webp/datasets.webp"
                  alt="Datasets" class="mb-6" img-height="300" img-width="300" id="b-card">
                  <b-card-text>
                    Subir y gestionar datasets. Iniciar un experimento con un dataset existente.
                  </b-card-text>
                </b-card>
              </a>

              <a href="/user-experiments">
                <b-card v-if="isAuthenticated" title="Mis Experimentos"
                  img-src="../assets/static/webp/laboratory.webp" alt="Experiments" size="sm" class="mb-4"
                  img-height="300" img-width="100" id="b-card">
                  <b-card-text>
                    Gestiona y visualiza de nuevo los experimentos que has creado.
                  </b-card-text>
                </b-card>
              </a>
            </b-card-group>
          </div>
        </b-col>
      </b-row>
    </div>
  </b-container>
</template>

<script>
export default {
  name: 'HomeUser',
  computed: {
    isAuthenticated() {
      return this.$store.getters['auth/isAuthenticated']
    },
    user() {
      return this.$store.getters['auth/user']
    }
  }
}
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
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
  max-width: 20rem;
  min-width: 20rem;
  min-height: 30rem;
  min-height: 30rem;
}

#go {
  box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
}
</style>