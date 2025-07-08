<template>
    <b-button @click="getExperimentWithDataset(dataset_id)" variant="outline-primary">
        {{this.method}}
    </b-button>
</template>

<script>
    import { getExperimentWithDatasetFromDB } from "@/api";
    export default{
        name: 'CreateExperimentButton',
        props : ['method', 'dataset_id'],
        methods: {
            async getExperimentWithDataset(){
                const response = await getExperimentWithDatasetFromDB(this.method, this.dataset_id, this.$store.getters['auth/jwtToken'])
                    .catch((error) => {
                        console.log(error.response);
                        if (error.response.status == 500) {
                            console.log("Error en el servidor");
                        }
                    });
                
                if (response.status === 200) {
                    if (["louvain", "girvan-newman"].includes(this.method)){
                        this.$store.commit('experiment/setExperiment', response.data);
                        this.$store.commit('experiment/setIsNewExperiment', true);
                    }
                    this.$router.push("/community-detection/"+this.method+"/experiment");
                }
                
            }
        }
    }
</script>