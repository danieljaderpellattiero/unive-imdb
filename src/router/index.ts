import HomeView from '../views/HomeView.vue'
import TitleView from '../views/TitleView.vue'
import SearchView from '../views/SearchView.vue'
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
      path: '/search/:title',
      name: 'search',
      component: SearchView,
      props: (route) => ({
        title: route.params.title,
        page: route.query.page
      })
    },
    {
      path: '/title/:id',
      name: 'title',
      component: TitleView,
      props: (route) => ({
        id: route.params.id,
        isEpisode: route.query.isEpisode === 'true'
      })
    }
  ]
})

export default router
