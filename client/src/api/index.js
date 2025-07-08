import axios from 'axios'

const API_URL = 'http://localhost:8181'

export function login(form){
    return axios.post(`${API_URL}/login`, form)
}

export function register_user(form){
    return axios.post(`${API_URL}/create-user`, form)
}

export function fetchExperimentsFromDB(jwt){
    return axios.get(`${API_URL}/get-experiments/`, {headers: {'Authorization': `Bearer: ${jwt}`}})
}

export function postExperimentToDB(experiment, jwt){
    return axios.post(`${API_URL}/save-experiment/`, experiment, {headers: {'Authorization': `Bearer: ${jwt}`}, 'Content-Type': 'application/json'})
}

export function deleteExperimentFromDB(experiment_id, jwt){
    return axios.delete(`${API_URL}/delete-experiment/${experiment_id}`,
        {headers: {'Authorization': `Bearer: ${jwt}`}})
}

export function postDatasetToDB(dataset, jwt){
    return axios.post(`${API_URL}/save-dataset`, dataset, {headers: {'Authorization': `Bearer: ${jwt}`}})
}

export function getDatasetsFromDB(jwt){
    return axios.get(`${API_URL}/get-datasets`, {headers: {'Authorization': `Bearer: ${jwt}`}})
}

export function deleteDatasetFromDB(dataset_id, jwt){
    return axios.delete(`${API_URL}/delete-dataset/${dataset_id}`,
        {headers: {'Authorization': `Bearer: ${jwt}`}})
}

export function postDatasetForExperiment(method, formData){
    var method_url = ''
    if (["louvain", "girvan-newman"].includes(method)){
        method_url = `/community-detection/${method}`
    }
    else if (method === "graph-visualization"){
        method_url = `/graph-visualization`
    }
    else{
        method_url = `/${method}`
    }
    const url = API_URL + method_url
    return axios.post(url,
        formData,
        {headers: {"Content-Type": "multipart/form-data"}}
    )
}

export function getExperimentWithDatasetFromDB(method, dataset_id, jwt){
    return axios.get(`${API_URL}/community-detection/${method}/${dataset_id}`, 
        {headers: {'Authorization': `Bearer: ${jwt}`}}
    )
}

export function getExperimentExample(){
    console.log("Peticion")
    return axios.get(`${API_URL}/community-detection/louvain/example`)
}
  