import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  },
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/stats',
      name: 'Stats',
      component: () => import('../views/StatsView.vue'),
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/about',
      name: 'About',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/tasks',
      component: () => import('../views/TasksView.vue'),
    },
    {
      path: '/projects',
      component: () => import('../views/ProjectsView.vue'),
    },
    {
      path: '/tags',
      component: () => import('../views/TagsView.vue')
    },
    {
      path: '/tags/:name',
      component: () => import('../views/TagView.vue')
    }
  ],
});

// Prevent to visit page that requiresAuth
// router.beforeEach((to) => {
//   if (to.meta.requiresAuth) {
//     return false
//   }
// })

export default router;
