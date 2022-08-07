import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/stats',
      name: 'Stats',
      component: () => import('../views/StatsView.vue')
    },
    {
      path: '/about',
      name: 'About',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/tasks',
      component: () => import('../views/TasksView.vue')
    },
    {
      path: '/projects',
      component: () => import('../views/ProjectsView.vue')
    },
  ]
})

export default router
