import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

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
      component: () => import('../views/TagsView.vue'),
    },
    {
      path: '/tags/:name',
      component: () => import('../views/TagView.vue'),
    },
  ],
});

router.beforeEach((to) => {
  // Prevent visit to register and login when auth
  if (to.name === 'Login' || to.name === 'Register') {
    const auth = useAuthStore();
    if (auth.isAuthenticated) {
      return { name: 'Home' };
    }
  }
});

export default router;
