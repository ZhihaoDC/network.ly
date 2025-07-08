import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index'
import Home from '../views/Home.vue'
import HomeUser from '../views/HomeUser.vue'
import CommunityDetection from '../views/CommunityDetection.vue'
import FormLouvain from '../views/FormLouvain.vue'
import FormDataset from '../views/FormDataset.vue'
import VisualizationExperiment from '../views/VisualizationExperiment.vue'
import UserExperiments from '../views/UserExperiments.vue'
import UserDatasets from '../views/UserDatasets.vue'
import UserSignUp from '../views/UserSignUp.vue'
import UserLoginModal from '../components/UserLoginModal.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    beforeEnter (to, from, next) {
      if (store.getters['auth/isAuthenticated']) {
        next('/home-user')
      } else {
        next()
      }
    }
  },
  {
    path: '/home-user',
    name: 'HomeUser',
    component: HomeUser
  },  
  {
    path: '/dataset-upload-form',
    name: 'FormDataset',
    component: FormDataset
  },
  {
    path: '/community-detection',
    name: 'CommunityDetection',
    component: CommunityDetection
  },
  {
    path: '/community-detection/louvain',
    name: 'FormLouvain',
    component: FormLouvain
  },
  {
    path: '/community-detection/girvan-newman',
    name: 'FormGirvanNewman',
    component: () => import('../views/FormGirvanNewman.vue')
  },
  {
    path: '/graph-visualization',
    name: 'FormVisualization',
    component: () => import( '../views/FormVisualization.vue')
  },
  {
    path: '/community-detection/:method/experiment',
    name: 'VisualizationExperiment',
    component: VisualizationExperiment
  },
  {
    path: '/user-experiments',
    name: 'UserExperiments',
    component: UserExperiments,
    beforeEnter (to, from, next) {
      if (!store.getters['auth/isAuthenticated']) {
        next('/user-login')
      } else {
        next()
      }
    }
  },
  {
    path: '/user-datasets',
    name: 'UserDatasets',
    component: UserDatasets,
    beforeEnter (to, from, next) {
      if (!store.getters['auth/isAuthenticated']) {
        next('/')
      } else {
        next()
      }
    }
  },
  {
    path: '/user-signup',
    name: 'UserSignUp',
    component: UserSignUp
  },
  {
    path: '/user-login',
    name: 'UserLoginModal',
    component: UserLoginModal
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
