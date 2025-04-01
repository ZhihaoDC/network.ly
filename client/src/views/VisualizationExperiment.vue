<template>
<b-container fluid id="parent-container" class="flex-grow-1"> 
      
    <b-row no-gutters>
        <b-col cols="3">
            <PlotNetworkForm 
                id="save-network-form" 
                ref="plotNetworkForm" 
                :activateSubmitButton="animation_finished"
                :communityColor="communityColor"
                @export-network="exportNetwork"  
                @updateVisualizationParameters="updateVisualizationParameters"
                @changeCommunityColor="changeCommunityColor"
                @updateEdgesColor="updateEdgesColor">
            </PlotNetworkForm>
        </b-col>
        <b-col cols="9">
            <PlotNetwork id="network-viz" ref="plotNetwork" @network-exported="submitExperiment"  @ready="animation_finished = true" :isNewExperiment="isNewExperiment"
            :visualizationParameters="visualizationParameters" @setSelectedColor="setSelectedColor"></PlotNetwork>
        </b-col>
        

    </b-row>
</b-container>
</template>

<script>
import PlotNetwork from "@/components/PlotNetwork.vue";
import PlotNetworkForm from "@/components/PlotNetworkForm.vue";
// import { mapGetters } from 'vuex';
export default {
    name: "VisualizationExperiment",
    components: { PlotNetwork, PlotNetworkForm },
    data: function () {
        return {
                experiment: this.$store.getters['experiment/getExperiment'],
                isNewExperiment: this.$store.getters['experiment/getIsNewExperiment'],
                visualizationParameters: this.$store.getters['experiment/getVisualizationParams'],
                animation_finished: false,
                communityColor: null
                };
    },
    methods: {
        exportNetwork(){
            this.$refs.plotNetwork.exportNetwork();
        },
        submitExperiment(){
            this.$refs.plotNetworkForm.submit_experiment_with_confirmation();
        },
        updateVisualizationParameters(newNetworkParams){
            console.log("VisualizationExperiment")
            console.log(newNetworkParams)
            this.visualizationParameters = newNetworkParams
        },
        setSelectedColor(selectedColor){
            this.communityColor = selectedColor
        },
        changeCommunityColor(new_color){
            this.communityColor = new_color
            this.$refs.plotNetwork.changeCommunityColor(new_color)
        },
        updateEdgesColor(){
            this.$refs.plotNetwork.updateEdgesColor()
        },
        toast_info(title, body, link_to=null, delay=10000){
            this.$bvToast.toast(body, {
            title: title,
            toaster: 'b-toaster-bottom-right',
            variant: 'info',
            //   noAutoHide: true,        
            autoHideDelay: delay,
            solid: true,
            appendToast: true,
            to: link_to
            })

        }

    },
    mounted() {
        console.log(this.experiment)

        if (this.isNewExperiment || (!this.user)){
            
            this.toast_info(`Tip 1:`, 'Puedes hacer zoom con la rueda de scroll del ratón');
            this.toast_info(`Tip 2:`, 'Selecciona nodos individuales con doble click', null, 10500)
            this.toast_info(`Tip 3:`, 'Pulsa la tecla Ctrl + click para seleccionar múltiples nodos.', null, 11000)
            
        }

    },
    computed: {
        // mapGetters('experiment', ['getExperiment', 'getIsNewExperiment', 'getVisualizationParams'])
        user() {
            return this.$store.getters['auth/user']
        }
    }

}
</script>

<style scoped>
    #title{
        position:absolute;  
        text-align: left;
    }

    #parent-container{
        /* padding-left: 20px;
        padding-right: 20px */
        margin-top: 1rem
    }

    #save-network-form{
        padding-top: 25px;
        border-top: 1em;
        border-radius: 15px;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px,
    rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
        
    }
    #network-viz{
        min-height: 90vh;
        z-index:1;
        border-radius: 10px;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px,
            rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
        margin-left: 1rem;
    }
    #page-title{
        position:absolute;
        z-index: 2;
        background-color:white;
        /* border-radius: 10px;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px,
            rgba(60, 64, 67, 0.15) 0px 1px 3px 1px; */
    }
</style>