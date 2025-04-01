<template>
  
    
  <b-form-group id="nw-parameters">
    <div>
      <b-label id="nwParam" for="nw-nodeSeparation" class="mb-1">Separacion de nodos</b-label>
      <b-form-input type="range" id="nw-nodeSeparation" size="sm" class="mb-2"
        v-model="visualizationParameters.nodeSeparation" min=1000 max=20000 step=1000 @input="emit_changes()"
      ></b-form-input>
    </div>

    <div v-if="isCommunityDetection">
      <b-label id="nwParam" for="nw-communitySeparation" class="mb-1">Separacion de comunidades</b-label>
      <b-form-input type="range" id="nw-communitySeparation" size="sm" class="mb-2"
        v-model="visualizationParameters.communitySeparation" min=100 max=5000 step=100 @input="emit_changes()"
      ></b-form-input>
    </div>

    <div>
      <b-label id="nwParam" for="nw-gravity" class="mb-1">Gravedad</b-label>
      <b-form-input type="range" id="nw-gravity" size="sm" class="mb-1" 
        v-model="visualizationParameters.gravity" min=0.1 max=1 step=0.1 @input="emit_changes()"
      ></b-form-input>
    </div>
 
  </b-form-group>
</template>


<script>
  export default {
    name: "PlotVisualizationParameters",
    props : ['isCommunityDetection'],
    data() {
      return {
          debounceTimer: null,
          changesQueue: [],
          visualizationParameters: this.$store.getters['experiment/getVisualizationParams']
      }
    },
    methods:{
      emit_changes() {
        var vizParams = this.visualizationParameters
        for (let key in vizParams) {
          vizParams[key] = parseFloat(vizParams[key]);
        }
        this.$store.commit('experiment/setVisualizationParams', vizParams)
        this.$emit('updateVisualizationParameters', vizParams)
      }
    }
  }
</script>

<style scoped>
#nwParam{
  text-align: left;
}
</style>