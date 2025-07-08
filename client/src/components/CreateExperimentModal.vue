<template>
    <b-button variant="primary" @click="openModal(row.item)">
        <b-icon icon="bounding-box" aria-hidden="true" scale="1" class="pt-1"></b-icon>
        Experimento
        <b-modal v-model="modalShow" :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
            <CreateExperimentButton method="louvain" :dataset_id="this.dataset_id" class="mr-4"></CreateExperimentButton>
            <CreateExperimentButton method="girvan-newman" :dataset_id="this.dataset_id"  ></CreateExperimentButton>
        </b-modal>
    </b-button>

</template>

<script>
import CreateExperimentButton from './CreateExperimentButton.vue';

    export default {
    name: "CreateExperimentModal",
    props: ["row"],
    data: function () {
        return {
            infoModal: {
                id: 'info-modal',
                title: '',
                content: '',
            },
            modalShow: false,
            selectedRowIndex: null,            
            dataset_id: null
        };
    },
    methods: {
        openModal(item) {
            this.infoModal.title = 'Selecciona un método de detección de comunidades';
            this.infoModal.content = JSON.stringify(item, null, 2);
            this.dataset_id = item.id
            this.modalShow = true;
        },
        resetInfoModal() {
            this.infoModal.title = '';
            this.infoModal.content = '';
        },
    },
    components: { CreateExperimentButton }
}
</script>