<template>
  <b-container fluid="md">
    <div id="community-detection">
      <h1 id="header">Detección de comunidades: Louvain</h1>
      <h4>
        Método basado en la medida de modularidad, que mide la diferencia en 
        densidad de las interconexiones intra-comunidad e inter-comunidad.
      </h4>
      <div id="content">
        <InputCSV selectedMethod="louvain" 
          action="experiment/getExperimentWithDataset" 
          successUrl="/community-detection/louvain/experiment"
        />
      </div>
    </div>
  </b-container>
</template>

<script>
import InputCSV from "@/components/InputCSV.vue";
export default {
  components: { InputCSV },
  name: "FormLouvain"
};
</script>

<style scoped>
</style>