<template>
  <b-container fluid="md">
    <div class="community-detection">
      <h1 id="header">Visualización de redes o grafos</h1>
      <h4>
        Visualiza la red, cambia los nodos de posición, color y físicas.
      </h4>
      <div id="content">
        <InputCSV selectedMethod="graph-visualization"
          action="experiment/getExperimentWithDataset"
          successUrl="/community-detection/graph-visualization/experiment"
        />
      </div>
    </div>
  </b-container>
</template>

<script>
import InputCSV from "@/components/InputCSV.vue";
export default {
  components: { InputCSV },
  name: "FormVisualization"
};
</script>

<style scoped>
</style>