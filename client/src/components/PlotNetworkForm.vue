<template>

  <b-container id="container" class="d-flex flex-column py-1 px-3">

    <h4 id="header" v-if='isCommunityDetection'> <b> Experimento detección de comunidades ({{ experiment.category }}) </b></h4> 
      <h4 id="header" v-else> <b> Visualización </b></h4>

    <b-form>
      <b-form-group class="mt-3">
        <h4 v-if="!editing" @click="startEditing" title="Nombre del experimento"> {{experiment_name}} 
          <b-icon id="edit-icon" icon="pencil-fill"></b-icon>
        </h4>

        <b-form-input v-else id="experiment_name" 
        ref="experiment_name_input" 
        class="custom-input" 
        v-model="experiment.experiment_name"
        @keyup.enter="stopEditing"
        @blur="stopEditing" 
        @focus="moveCursorToLeft"
        :placeholder="experiment_name">
        </b-form-input>
      </b-form-group>

      <b-form-group id="input-description" label="Descripción" label-for="input-description">
        <b-form-textarea id="description" v-model="experiment.description" @change="updateDescription"
          placeholder="Introduce una descripción para el experimento"></b-form-textarea>
      </b-form-group>


      <PlotVisualizationParameters @updateVisualizationParameters="updateVisualizationParameters" :isCommunityDetection="isCommunityDetection"></PlotVisualizationParameters>


      <b-form-group v-if='isCommunityDetection' id="input-communityColor" class="mb-3" >
        <label id="colorPickerLabel" for="colorPicker">Color de la comunidad</label>
        <b-form-input id="colorPicker" type="color" v-model="communityColor" @input="changeCommunityColor()" @blur="updateEdgesColor()"></b-form-input>
      </b-form-group>       

    </b-form>
    <div id="submit-experiment">
      <b-button id="submit-experiment" block size="lg" type="submit" :disabled="!(activateSubmitButton && isAuthenticated)" @click="handleSubmitNetwork" variant="primary"
        class="content-item submit-button mt-auto" >
        {{this.submitted_msg}}
      </b-button>
    </div>
    <b-popover v-if=!isAuthenticated target="submit-experiment" triggers="hover" placement="right">
      <template #title>¿Sabías que...?</template>
      Si te <b> registras,</b> podrás guardar el resultado de tus experimentos. Además de poder guardar y gestionar tus datasets.
      <b-link to="/user-signup"> Crea una cuenta aquí.</b-link>
    </b-popover>

    <div id="success-alert">
      <b-alert :show="dismissCountDown" dismissible fade variant="success" @dismissed="dismissCountDown=0"
        @dismiss-count-down="countDownChanged">
        ¡Experimento guardado! 
        <router-link to="/user-experiments" id="experiments-link">Ir a experimentos</router-link>
      </b-alert>

    </div>
    
  </b-container>

</template>

<script>
import PlotVisualizationParameters from "@/components/PlotVisualizationParameters.vue"

export default {
  name: "PlotNetworkForm",
  components: {PlotVisualizationParameters},
  props: ['activateSubmitButton', 'communityColor'],
  data: function () {
    return {
      experiment: this.$store.getters['experiment/getExperiment'],
      experiment_name: this.$store.getters['experiment/getExperiment'].experiment_name,
      user_id : 1,
      editing: false,
      dismissSecs: 4,
      dismissCountDown: 0,
      submitted_msg: "Guardar experimento",
      visualizationParameters: this.$store.getters['experiment/getVisualizationParams']
    }
  },
  methods: {
    startEditing(){
      this.editing = true
      this.experiment.experiment_name = this.experiment_name
      this.$nextTick(() => {
        this.$refs.experiment_name_input.$el.setSelectionRange(0, 0)
        this.$refs.experiment_name_input.focus()
      })
    },
    stopEditing(){
      this.editing = false
      if ((this.experiment.experiment_name !== this.experiment.dataset_name) & (this.experiment.experiment_name !== "")){
        this.experiment_name = this.experiment.experiment_name
        this.$store.commit('experiment/setExperimentName', this.experiment_name)
      }
    },  
    moveCursorToLeft() {
      const inputElement = this.$refs.experiment_name_input.$el;
      inputElement.setSelectionRange(0, this.experiment.experiment_name.length);
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    updateDescription(){
      this.$store.commit('experiment/setExperimentDescription', this.experiment.description)
    },
    showSuccessAlert() {
      this.dismissCountDown = this.dismissSecs
    },
    updateVisualizationParameters(newvisualizationParameters){
        this.visualizationParameters = newvisualizationParameters
        this.experiment.visualization_params = newvisualizationParameters
        this.$emit('updateVisualizationParameters', newvisualizationParameters)
    },
    async handleSubmitNetwork(){
      // console.log("Mandando señal para actualizar experimento...")
      this.$emit("export-network")
    },
    submit_experiment_with_confirmation() {
      //Ask confirmation
      // console.log("Subiendo experimento")
      if (this.experiment.experiment_id != null) {
        this.$bvModal.msgBoxConfirm('Guardar de nuevo experimento sobreescribirá el antiguo. ¿Quieres sobreescribir el experimento anterior?', {
          title: '¿Sobreescribir experimento?',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'primary',
          okTitle: 'Sobreescribir',
          cancelTitle: 'Cancelar',
          footerClass: 'p-2',
          hideHeaderClose: false,
          centered: true
        })
          .then(confirmation => {
            if (confirmation){
              this.submit_experiment_to_backend()
            }
          })
          .catch(err => {
            // An error occurred
            console.log(`Error: ${err}`)
          })
      }
      if (!this.confirmation && (this.experiment.experiment_id == null)) {
        this.submit_experiment_to_backend()
      }
    },

    async submit_experiment_to_backend() {
      this.experiment = this.$store.getters['experiment/getExperiment']
      await this.$store.dispatch('experiment/saveExperiment')      
      this.experiment = this.$store.getters['experiment/getExperiment']
      // console.log("Saving experiment:")
      // console.log(this.experiment)
      this.submitted_msg = "Guardado!"
      this.showSuccessAlert()
    }, 

    changeCommunityColor(){
      this.$emit('changeCommunityColor', this.communityColor)
    },
    updateEdgesColor(){
      this.$emit('updateEdgesColor')
    }
  
  },
  computed: {
      isAuthenticated() {
        return this.$store.getters['auth/isAuthenticated']
      },
      isCommunityDetection(){
        return ["Louvain", "Girvan-Newman"].includes(this.experiment.category)
      }

    }
}
</script>

<style scoped>

#container{
  margin-left: 1rem;
}
.custom-input{
  border: none;
  box-shadow: none;
  outline: none;
  font-size: 1.5rem;
  text-align: center;
}

#input-name,
#input-description {
  text-align: left;
}

#edit-icon{
  padding-bottom: 0.15em;
  padding-top: 0.1em;
  padding-left: 0.05em;
  padding-right: 0.1em;
}
#success-alert {
  padding-top: 15px;
  padding-bottom: 5px;
}
</style>