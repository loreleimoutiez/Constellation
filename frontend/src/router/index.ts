import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/assets',
      name: 'assets',
      component: () => import('../views/AssetsView.vue'),
    },
    {
      path: '/assets/:id',
      name: 'asset-detail',
      component: () => import('../views/AssetDetailView.vue'),
    },
    {
      path: '/assets/new',
      name: 'asset-new',
      component: () => import('../views/AssetFormView.vue'),
    },
    {
      path: '/graph',
      name: 'graph',
      component: () => import('../views/GraphView.vue'),
    },
    {
      path: '/impact',
      name: 'impact',
      component: () => import('../views/ImpactView.vue'),
    },
  ],
})

export default router
