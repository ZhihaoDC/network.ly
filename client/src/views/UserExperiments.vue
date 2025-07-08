<template>
    <b-container fluid="md">
        <div>
            <h1 id="header"> Experimentos </h1>
            <h4> Aquí encontrarás los experimentos que realices y que hayas guardado. </h4>
            <br/>
        </div>
        <div>
            <Experiments></Experiments>
        </div>
    </b-container>
</template>


<script>
import Experiments from "@/components/Experiments.vue";
export default{
    name: "UserExperiments",
    components: {Experiments}
}
</script>


<style>

</style>