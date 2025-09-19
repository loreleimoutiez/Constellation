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
      path: '/assets/:id/edit',
      name: 'asset-edit',
      component: () => import('../views/AssetFormView.vue'),
    },
    {
      path: '/relations',
      name: 'relations',
      component: () => import('../views/RelationsView.vue'),
    },
    {
      path: '/impact',
      name: 'impact',
      component: () => import('../views/ImpactView.vue'),
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('../views/ReportsView.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
    },
  ],
})

export default router
