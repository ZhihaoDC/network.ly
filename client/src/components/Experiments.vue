<template>
    <div id="experiments-container">
        <div v-if="!isFetching">
            <div v-if="((experiments != null) && (Object.keys(experiments).length != 0))">
                <b-card-group v-for="(experiments, idx) in makeRows" :key="idx" deck
                    class="align-items-center justify-content-center">
                    <b-card v-for="(experiment, index) in experiments" :key="index" class="mb-3" id="b-card"
                        :title="experiment.experiment_name" :sub-title="experiment.category" :img-src="'data:image/png;base64,' +  experiment.thumbnail">
                        <!-- <b-img fluid :src="'data:image/png;base64,' +  experiment.thumbnail"></b-img> -->
                        <b-card-text v-if="experiment.description"> {{ experiment.description }} </b-card-text>
                        <b-card-text v-else id="missing-description"> No hay descripción </b-card-text>
                        
                        <b-button v-if="!submitted" @click="visualize(experiment)"
                        value="Visualizar" type="submit" variant="primary" class="mr-2">
                            Visualizar
                        </b-button>
                        <b-spinner v-else variant="primary" label="Spinning" id="spinner" class="m-5"></b-spinner>
                        <b-button @click="delete_experiment(experiment)"
                        value="Eliminar" variant="outline-danger">
                            <!-- Eliminar -->
                            <b-icon icon="trash" aria-hidden="true" scale="1.1" class="pt-1"></b-icon>
                        </b-button>
                

                        <template #footer>
                            <small class="text-muted">Creado el {{parseDate(experiment.creation_date)}}</small>
                        </template>

                    </b-card>
                </b-card-group>
            </div>
            <div v-else id="empty-experiments-container">
                <b-img id="empty-experiments-img" src="../assets/static/test-tube2.png" alt="No hay experiments" :width="200" :height="200"/> 
                <div> No hay experimentos todavía </div>
            </div>
        </div>
    </div>
</template>

<script>
import {fetchExperimentsFromDB, deleteExperimentFromDB} from '@/api'

export default {
    name: "Experiments",
    data: function () {
        return {
            experiments: [],
            submitted: false,
            isFetching: true,
            user_id: 1,
            n_experiments: 0,
            number_experiment_columns: 4,
        };
    },
    computed: {

        makeRows() {
            let row = [];
            let rowSize = this.number_experiment_columns
            let i, l, chunkSize = rowSize;
            for (i = 0, l = this.n_experiments; i < l; i += chunkSize) {
                row.push(this.experiments.slice(i, i + chunkSize));
            }
            console.log(row)
            return row
        }
    },

    methods: {
        getExperiments() {
            fetchExperimentsFromDB(this.$store.getters['auth/jwtToken'])
                .then((response) => {
                    this.experiments = response.data.experiments
                    this.n_experiments = this.experiments.length
                    let n_rows = this.n_experiments / this.number_experiment_columns
                    this.number_experiment_rows = Math.floor(n_rows) + 1
                    this.isFetching = false
                })
                .catch((error) => {
                    console.error(error)
                })

        },

        parseDate(date) {
            const db_date = new Date(date);
            const local_date = new Date((db_date) - (db_date.getTimezoneOffset() * 60 * 1000))
            const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', seconds: 'numeric', hour12: false }
            return local_date.toLocaleString('es-ES', options)
        },

        visualize(experiment) {
            this.submitted = true
            this.$store.commit('experiment/setExperiment', experiment);
            this.$store.commit('experiment/setIsNewExperiment', false);
            this.$router.push(`/community-detection/${experiment.category.toLowerCase()}/experiment`);
        },

        delete_experiment(experiment) {
            this.$bvModal.msgBoxConfirm('La siguiente acción borrará el experimento. ¿Estás seguro?', {
                title: '¿Eliminar experimento?',
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
                        const id_to_remove = experiment.experiment_id
                        deleteExperimentFromDB(id_to_remove, this.$store.getters['auth/jwtToken'])
                            .then(response => {
                                if (response.status === 200) {
                                    console.log(response)
                                    this.experiments = this.experiments.filter((experiment) => {
                                        return experiment.experiment_id != id_to_remove});
                                }
                            })
                            .catch(error => {
                                console.log(error)
                            })
                    }
                })

        }

    },

    beforeMount() {
        this.getExperiments(); //get experiments from backend

    }


}

</script>

<style scoped lang="scss">
#b-card {
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
    max-width: 20rem;
};

@media screen and (min-width: 20em) {
  .card-img,
  .card-img-top,
  .card-img-bottom {
    min-height: 15em !important;
    padding: 0.5em
  }
}
// #delete-button {
//     color: gray;
//     font-size: 0.8rem;
//     text-decoration: underline;
// };

// #delete-button:hover {
//     color: crimson
// };

#empty-experiments-container{
    padding:2em;
}
#empty-experiments-img{
    vertical-align: middle;
    padding: 1.25em;
}
#missing-description{
    color: gray;
    font-style: italic;
    font-size: small
}

</style>