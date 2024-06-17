import HomeView from '../views/HomeView.vue'
import TitleView from '../views/TitleView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/title/:id',
      name: 'title',
      component: TitleView
    }
  ]
})

export default router
