<template>
<b-container fluid> 
    <h2 id="header" v-if='((experiment.category === "Louvain") | (experiment.category === "Girvan-Newman"))'> Algoritmo de {{ experiment.category }} </h2> 
    <h2 id="header" v-else> Visualización </h2>  
    <PlotNetwork :experiment="experiment" @ready="animation_finished = true"></PlotNetwork>
    <PlotNetworkSave :experiment="experiment" :activateSubmitButton="animation_finished"></PlotNetworkSave>
</b-container>
</template>

<script>
import PlotNetwork from "@/components/PlotNetwork.vue";
import PlotNetworkSave from "@/components/PlotNetworkSave.vue";
import { store } from "../main.js";
export default {
    name: "VisualizationExperiment",
    components: { PlotNetwork, PlotNetworkSave },
    data: function () {
        return {
                experiment: store.state.lastComputedExperiment,
                animation_finished: false,
                };
    },
    mounted(){
        console.log(this.experiment)
    }
}

</script>

<style scoped>

    #title{
    position:absolute;  
    text-align: left;
    }

</style>