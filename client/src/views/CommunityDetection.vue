<template>
    <b-container fluid>
        <h1 id="header"> Detección de comunidades </h1>
        <h4> Introducir un dataset con formato y aplicar detección de comunidades.  </h4>
        <router-link to="/about" id="about-link">Aprende más sobre la detección de comunidades</router-link>
        <br/>
        <br/>

        <div class="tools">
          <h4> Elige un método de detección de comunidades:</h4>
          <b-card-group deck>
            <b-card
            title="Método de Louvain"
            class="mb-3"
            id="b-card">
              <b-card-text>
                El más popular. Rápido y preciso. Las comunidades detectadas pueden variar entre ejecuciones.
              </b-card-text>
              <b-button block to="/community-detection/louvain" variant="primary" id="go">Ir</b-button>
            </b-card>
  
            <b-card
            title="Método de Girvan-Newman"
            class="mb-3"
            id="b-card">
              <b-card-text>
                Método clásico y que produce resultados más estables. En todas las ejecuciones, las comunidades son iguales.
              </b-card-text>
              <b-button block to="/community-detection/girvan-newman" variant="primary" id="go">Ir</b-button>
            </b-card>
            
          </b-card-group>
        </div>
        
    </b-container>
  </template>
  
  <script>
  export default {
    name: 'CommunityDetection'
  }
  </script>
  
  <style scoped>
  
    #start-button{
      padding: 0.5em 0.7em;
    }
  
    #about-link{
      color: #42b983;
      text-decoration: none;
    }
  
    
    #section-header{
        padding-top: 2rem;
        padding-bottom:1rem;
    }
  
    #b-card{
      box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
      max-width: 25rem;
    }
  
    #go{
      box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
    }
  </style>