<template>
    <b-container fluid="md">
        
      <div id="community-detection">
        <h1 id="header">Datasets</h1>
        <h4>
          Introduce tu dataset.
        </h4>
        <div id="content">
          <InputCSV selectedMethod="dataset" action="experiment/postDataset" successUrl="/user-datasets"/>
        </div>
      </div>
    </b-container>
  </template>
  
  <script>
  import InputCSV from "@/components/InputCSV.vue";
  export default {
    components: { InputCSV },
    name: "FormDataset",
  };
  </script>
  
  <style scoped>
  </style>