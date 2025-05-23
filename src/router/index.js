import Vue from 'vue'
import VueRouter from 'vue-router'
import indexView from '../views/index.vue'
import riskPerson from '@/views/riskPerson.vue'
import riskTask from '@/views/riskTask.vue'
import mappingKnowledge from '@/views/mappingKnowledge.vue'
import opinionInformation from '@/views/opinionInformation.vue'
import campusOpinion from '@/views/campusOpinion.vue'
import schoolOpinion from '@/views/schoolOpinion.vue'
import mappingKnowledge1 from '@/views/mappingKnowledge1.vue'
import schoolOpinion1 from '@/views/schoolOpinion1.vue'
import riskPerson1 from '@/views/riskPerson1.vue'
import riskTask1 from '@/views/riskTask1.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: indexView,
    redirect: '/campusOpinion',
    children: [{
      path: '/riskPerson',
      component: riskPerson
    },
    {
      path: '/riskTask',
      component: riskTask
    },
    {
      path: '/mappingKnowledge',
      component: mappingKnowledge
    },
    {
      path: '/opinionInformation',
      component: opinionInformation
    },
    {
      path: '/campusOpinion',
      component: campusOpinion
    },
    {
      path: '/schoolOpinion',
      component: schoolOpinion
    }
    ]
  },
  {
    path: '/riskPerson1',
    component: riskPerson1
  },
  {
    path: '/schoolOpinion1',
    component: schoolOpinion1
  },
  {
    path: '/mappingKnowledge1',
    component: mappingKnowledge1
  },
  {
    path: '/riskTask1',
    component: riskTask1
  }
]

const router = new VueRouter({
  routes
})

export default router
