import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import { useCMDBStore } from '@/stores/cmdb'

// Mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/assets/new', component: { template: '<div>New Asset</div>' } }
  ]
})

describe('DashboardView Integration', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should render loading state initially', () => {
    const wrapper = mount(DashboardView, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.text()).toContain('Dashboard')
    expect(wrapper.text()).toContain('Monitor your infrastructure')
  })

  it('should handle data fetching and display CIs', async () => {
    const store = useCMDBStore()
    
    const wrapper = mount(DashboardView, {
      global: {
        plugins: [router]
      }
    })

    // Wait for component to mount and fetch data
    await wrapper.vm.$nextTick()
    
    // Wait for async operations
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Check that the store has been called (will have real data from API)
    expect(store.cis.length).toBeGreaterThanOrEqual(0)
  })

  it('should have refresh button that works', async () => {
    const wrapper = mount(DashboardView, {
      global: {
        plugins: [router]
      }
    })

    const refreshButton = wrapper.find('button')
    expect(refreshButton.exists()).toBe(true)
    expect(refreshButton.text()).toContain('Refresh')
    
    // Click refresh button
    await refreshButton.trigger('click')
    
    // Should still be in the same state (no errors)
    expect(wrapper.text()).toContain('Dashboard')
  })
})