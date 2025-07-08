<template>
    <b-container fluid="md">
        <h1 id="header">Datasets guardados</h1>
        <h4>
        Aquí encontrarás los datasets que has guardado. También puedes crear nuevos experimentos.
        </h4>
        <div v-if="((datasets != null) && (Object.keys(datasets).length != 0))">
            <b-table
                id="my-table"
                class="mt-3" outlined
                :items="datasets"
                :fields="fields"
                :per-page="perPage"
                :current-page="currentPage"
            >
                <template #cell(actions)="row">
                    <col :style="{ width: '10em'}" >
                        <div class="buttons">
                        
                        <CreateExperimentModal class="mr-2 pt-1" :row="row"></CreateExperimentModal>
                        <b-button @click="delete_dataset(row.item.id)" value="Eliminar" variant="outline-danger">
                            <b-icon icon="trash" aria-hidden="true" scale="1.1" class="pt-1"></b-icon>
                        </b-button>
                        
                        </div>
                </template>

            </b-table>

            <b-pagination
                v-model="currentPage"
                :total-rows="rows"
                :per-page="perPage"
                aria-controls="my-table"
                size="sm"
                align="right"
            ></b-pagination>    
        </div>
        
        <div v-else id="empty-datasets-container">
            <b-img id="empty-datasets-img" src="../assets/static/database-empty.png" alt="No hay datasets" :width="200" :height="200"/>
            <p> Aún no hay datasets subidos</p>
        </div>
        <b-button variant="primary" to="/dataset-upload-form">
            <b-icon icon="plus" aria-hidden="true"></b-icon> Añadir un dataset
        </b-button>
    </b-container>
</template>
  
<script>
import CreateExperimentModal from '@/components/CreateExperimentModal.vue';
import { getDatasetsFromDB, deleteDatasetFromDB } from '../api';

    export default {
    name: 'UserDatasets',
    components: {CreateExperimentModal},
    data() {
        return {
            user_id: 1,
            perPage: 3,
            currentPage: 1,
            datasets: [],
            fields: [
                { key: 'name', label: 'Nombre del dataset' },
                { key: 'creation_date', label: 'Fecha de creación' },
                { key: 'nodes', label: 'Ejemplo de nodos' },
                { key: 'actions', label: 'Acciones'}
            ]
        };
    },
    computed: {
        rows() {
            return this.datasets.length;
        }
    },
    mounted() {
        getDatasetsFromDB(this.$store.getters['auth/jwtToken'])
            .then((response) => {
            if (response.status === 200) {
                this.datasets = response.data['datasets'];
                this.datasets = this.format_datasets(this.datasets);
                console.log(this.datasets);
            }
        })
            .catch((error) => {
            console.log(error);
            if (error.status == 500) {
                this.error =
                    "Formato erróneo. Por favor, introduce un .csv con las columnas en orden: \n " +
                        "from, to, weight";
            }
        });
    },
    methods: {
        format_dataset(dataset) {
            let dataset_nodes = dataset.json.elements.nodes.map(node => node.data.name);
            let dataset_json = {
                name: dataset['name'],
                id: dataset['id'],
                creation_date: this.parseDate(dataset['creation_date']),
                nodes: dataset_nodes.join(', ').substring(0, 50) + " ..."
            };
            return dataset_json;
        },
        format_datasets(datasets) {
            let formatted_dataset = datasets.map(dataset => this.format_dataset(dataset));
            return formatted_dataset;
        },
        parseDate(date) {
            const db_date = new Date(date);
            const local_date = new Date((db_date) - (db_date.getTimezoneOffset() * 60 * 1000))
            const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', seconds: 'numeric', hour12: false }
            return local_date.toLocaleString('es-ES', options)
        },
        toast_on_delete(){
            this.$bvToast.toast('Dataset eliminado con éxito.', {
            title: `Exito.`,
            variant: 'info',
            solid: true
            })
        },
        delete_dataset(dataset_id){
            const h = this.$createElement
            const msgBox = h('p', {class: ['msgBoxtext']},[
                'La siguiente acción borrará el dataset. ', 
                h('strong', {class: ['danger-delete']}, 'También borrará todos sus experimentos asociados. \n'),
                h('br'),
                h('b', {class: ['dark']}, '¿Estás seguro?')
            ])
            this.$bvModal.msgBoxConfirm(msgBox, {
                title: '¿Eliminar dataset?',
                size: 'sm',
                buttonSize: 'sm',
                okVariant: 'danger',
                okTitle: 'Eliminar',
                cancelTitle: 'Cancelar',
                footerClass: 'p-2',
                hideHeaderClose: false,
                centered: true
            })
                .then(action => {
                    if (action) {
                        var id_to_remove = dataset_id
                        deleteDatasetFromDB(dataset_id, this.$store.getters['auth/jwtToken'])
                            .then(response => {
                                if (response.status === 200) {
                                    console.log(response)
                                    const to_remove = this.datasets.filter((dataset) => dataset.dataset_id == id_to_remove)
                                    this.datasets.splice(this.datasets.indexOf(to_remove), 1)
                                    // https://github.com/bootstrap-vue/bootstrap-vue/issues/4668
                                    // Array does not update to b-table because array are interpreted as references 
                                    // and watchers do not watch the content of the array
                                    this.toast_on_delete()
                                }
                            })
                            .catch(error => {
                                console.log(error)
                            })
                    }
                })

            
        }
    }
}
</script>
<style>
.buttons{
    display:inline-block
}
#add-dataset-link{
    color: #42b983;
    text-decoration: none;
}
.danger-delete{
    color:red
}
#empty-datasets-container{
    padding-top:2em;    
}
#empty-datasets-img{
    vertical-align: middle;
    padding: 1.25em;
}
</style>