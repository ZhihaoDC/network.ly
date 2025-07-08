<template>
  <div id="content-item">
    <label
      id="file-upload-label"
      for="file-upload"
      class="upload-button"
      v-bind:class="{ file_selected: file }"
      
    >
    <!-- v-b-popover.hover.right="'El contenido debe de ser una lista de enlaces (de la siguiente forma):\n' + 
        '\nColumna 1: Nodo origen del enlace' +
        '\nColumna 2: Nodo destino del enlace' +
        '\nColumna 3: Peso del enlace'"
      title="Formato del csv" -->
    
      <span>
        {{
          file
            ? "Archivo seleccionado: " + file.name
            : "Seleccionar un archivo (.csv)"
        }}
        <small>{{ file ? "(" + bytesToSize(file.size) + ")" : "" }}</small>
      </span>
    </label>

    <b-form-file
      id="file-upload"
      plain
      v-model="file"
      accept=".csv"
      required="required"
      enctype="multipart/form-data"
      @input="check_file()"
      ref="file_input"
    ></b-form-file>

    <b-popover target="file-upload-label" triggers="hover" placement="bottom">
      <template #title>Formato de input</template>
      El input deberá ser una <b>lista de enlaces</b> en formato <b>.csv</b> conteniendo: 
      <ul>
        <li> <b>Columna 1:</b> Nodo origen del enlace.</li>
        <li> <b>Columna 2:</b> Nodo destino del enlace. </li>
        <li> <b>Columna 3:</b> Peso del enlace. </li>
      </ul>
    </b-popover>
    <br />

    <small>
      Pon el cursor encima del botón para ver el formato del .csv
    </small>
    <br />

    <b-container fluid class="bv-example-row" v-if="!submitted">
      <b-form-checkbox
      class="content-item"
        v-model="manually_select_columns"
        name="check-button"
        switch
        v-bind:disabled="!(file && error.length === 0)"
      >
        Seleccionar columnas manualmente (nodo_origen, nodo_destino, peso)
      </b-form-checkbox>
      <b-row align-h="center" v-if="manually_select_columns">
        <b-form-group
          class="mx-4"
          id="content-item"
          label="Nodo origen"
          v-slot="{ ariaDescribedby }"
        >
          <b-form-radio-group
            id="source-node"
            v-model="source"
            v-on:change="update_currently_selected_columns(source, 'source')"
            :options="columns"
            :aria-describedby="ariaDescribedby"
            button-variant="outline-primary"
            size="sm"
            name="radio-btn-outline"
            buttons
            stacked
          ></b-form-radio-group>
        </b-form-group>

        <b-form-group
          id="content-item"
          class="mx-4"
          label="Nodo destino"
          v-slot="{ ariaDescribedby }"
        >
          <b-form-radio-group
            id="target-node"
            v-model="target"
            v-on:change="update_currently_selected_columns(target, 'target')"
            :options="columns"
            :aria-describedby="ariaDescribedby"
            button-variant="outline-success"
            size="sm"
            name="radio-btn-outline"
            buttons
            stacked
          ></b-form-radio-group>
        </b-form-group>
        <b-form-group
          id="content-item"
          class="mx-4"
          label="Peso arista"
          v-slot="{ ariaDescribedby }"
        >
          <b-form-radio-group
            id="weight"
            v-model="weight"
            v-if="columns.length > 2"
            v-on:change="update_currently_selected_columns(weight, 'weight')"
            :options="columns"
            :aria-describedby="ariaDescribedby"
            button-variant="outline-danger"
            size="sm"
            name="radio-btn-outline"
            buttons
            stacked
          ></b-form-radio-group>
        </b-form-group>
      </b-row>
    </b-container>
    <p>
      <small class="error" v-if="error.length != 0">{{ error }}</small>
    </p>
    <b-button
      type="submit"
      variant="primary"
      class="w-25 content-item submit-button"
      v-bind:disabled="!(file && !error)"
      value="Visualizar"
      v-on:click="validate_and_submit()"
      v-if="!submitted && isExperiment"
    >
    Visualizar 
    </b-button>
    <b-button
      type="submit"
      variant="primary"
      class="w-25 content-item submit-button"
      v-bind:disabled="!(file && !error)"
      value="Visualizar"
      v-on:click="validate_and_submit()"
      v-if="!submitted && (!isExperiment)"
    >
    Subir 
    </b-button>
    <b-spinner
      v-if="submitted"
      variant="primary"
      label="Spinning"
      id="spinner"
      class="m-5"
    ></b-spinner>
  </div>
  

</template>

<script>

import {EventBus} from '../main'
export default {
  name: "InputCSV",
  props: ["selectedMethod", "action", "successUrl"],
  data() {
    return {
      file: null,
      method: this.selectedMethod,
      manually_select_columns: false,
      columns: [], //options
      source: null,
      target: null,
      weight: null,
      currently_selected_columns: {
        'source': null,
        'target': null,
        'weight': null
      },
      error: "",
      submitted: false,
    };
  },
  methods: {

    check_file() {
      //Reset variables
      this.error = "";
      this.columns = [];
      let self = this

      const accepted_file_types = ["text/csv", "application/vnd.ms-excel"]

      if (!accepted_file_types.includes(this.file["type"]))
        this.error = "El archivo debe tener extensión .csv";
      else {
        this.read_file(this.file)
          .then(result => {
            let first_line = result.split("\n")[0]
            let headers = first_line.split(",")

            headers.forEach(header =>{
              let column = header.toString().replaceAll('"','').replaceAll("'", "")
              self.columns.push({text: column, value: column, disabled: false})})

            if (self.columns.length < 2)
              self.error = "Formato erróneo. Por favor, introduce un csv con al menos 3 columnas." 
          })
          .catch( () => {self.error = "Error desconocido"})
      } 
    },

    read_file(file){
      return new Promise((resolve, reject) => {
        var reader = new FileReader()
        reader.readAsText(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = () => reject
      })
    },

    
    validate_and_submit(){
      if (this.manually_select_columns && this.manual_columns_error)
        this.error = this.manual_columns_error
      else
        this.submit_file()
    },

    async submit_file(){
      var formData = new FormData()
      formData.append("file", this.file)

      if (this.manually_select_columns){
        formData.append("columns", new Blob([this.currently_selected_columns], {type: 'application/json'}));
      }
      this.submitted = true
      await this.$store.dispatch(this.action, {method: this.method, formData: formData})
      this.$router.push(this.successUrl);
    },

    // check_manually_selected_columns_and_submit(file){
    //   if (this.manually_select_columns){
    //     if ((this.source === null) || (this.target === null) || (this.weight === null)){
    //       this.error = "Por favor, rellena todos los valores correspondientes a nodo origen, destino y peso de arista"
    //     } else {
    //       this.error = ''
    //     }
    //   }
    //   if (!this.error){
    //     this.submit_file(file)
    //   }
    // },

    // format_columns(){
    //   return JSON.stringify({"source": this.source,
    //                           "target": this.target,
    //                           "weight": this.weight})
    // },

    // async submit_file() {
    //   this.submitted = true;
    //   let formData = new FormData();
    //   formData.append("file", this.file);
    //   if (this.manually_select_columns){
    //     var columns = this.format_columns()
    //     const columns_blob = new Blob([columns], {type: 'application/json'});
    //     formData.append("columns", columns_blob);
    //   }

    //   await this.$store.dispatch(this.action, {method: this.method, formData: formData})
    
    //   this.$router.push(this.successUrl);
        
    // },

    update_currently_selected_columns(element, clicked){
      //remove value from currently selected columns if value has already been chosen
      if (Object.values(this.currently_selected_columns).includes(element)){
        let key = Object.keys(this.currently_selected_columns).find(key => this.currently_selected_columns[key] === element)
        this.currently_selected_columns[key] = null
      }
      //update form variables
      this.currently_selected_columns[clicked] = element
      this.source = this.currently_selected_columns['source']
      this.target = this.currently_selected_columns['target']
      this.weight = this.currently_selected_columns['weight'] 
      this.error = ''
    },

    bytesToSize(bytes) {
      var sizes = ["Bytes", "KB", "MB", "GB", "TB"];
      if (bytes == 0) return "0 Byte";
      var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
      return Math.round(bytes / Math.pow(1024, i), 2) + " " + sizes[i];
    },
  },
  computed:{
    manual_columns_error() {
      const selected_cols = this.currently_selected_columns
      const source = selected_cols.source
      const target = selected_cols.target
      const weight = selected_cols.weight

      if (this.manually_select_columns && source && target && weight)
        return ""
      else{
        return "Por favor, rellena todos los valores correspondientes o desactiva la selección manual."
      }
    },
    isExperiment(){
      return ["louvain", "girvan-newman"].includes(this.selectedMethod)
    }
  },
  mounted(){
    EventBus.$on('csvFormatError', () =>{      
      this.submitted = false
      this.errorMessage = "Ha ocurrido un error procesando el archivo csv. Por favor, cambia el formato."
    })
  },
  beforeDestroy () {
      EventBus.$off('failedSignUp')
  }
};
</script>

<style scoped>
input[type="file"] {
  display: none;
}

#file-upload {
  align-items: center;
  width: 60%;
}

.upload-button {
  display: inline-block;
  color: aliceblue;
  background: #42b983;
  font-size: x-large;
  border-radius: 10px;
  padding: 0.7em 1em;
  margin-bottom: 0.2em;
  cursor: pointer;
  box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
}

.upload-button:hover {
  background-color: #050517;
  color: aliceblue;
  text-decoration: none;
}

.submit-button {
  font-size: large;
  box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
}
.submit-button:disabled {
  background-color: #c0c2c8;
  border: 0.5px solid #ccc;
  cursor: not-allowed;
}

.file_selected {
  background-color: #050517;
  color: aliceblue;
}
.error {
  color: red;
}

#spinner {
  width: 3rem;
  height: 3rem;
}
</style>
