<template>
  <div id="app" class="flex h-screen bg-gray-50">
    <!-- Mobile menu overlay -->
    <div 
      v-if="isMobileMenuOpen" 
      class="fixed inset-0 bg-gray-600 bg-opacity-75 z-20 lg:hidden"
      @click="isMobileMenuOpen = false"
    ></div>
    
    <!-- Sidebar -->
    <aside 
      :class="[
        'fixed inset-y-0 left-0 z-30 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
        isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full',
        isSidebarCollapsed ? 'lg:w-16' : 'lg:w-64'
      ]"
    >
      <!-- Logo & Brand -->
      <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          <span v-if="!isSidebarCollapsed" class="text-xl font-bold text-gray-900">Constellation</span>
        </div>
        <button 
          @click="isSidebarCollapsed = !isSidebarCollapsed"
          class="hidden lg:block p-1.5 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline :points="isSidebarCollapsed ? '9 18 15 12 9 6' : '15 18 9 12 15 6'" />
          </svg>
        </button>
      </div>

      <!-- Navigation -->
      <nav class="mt-8 px-4 space-y-6">
        <div>
          <h3 v-if="!isSidebarCollapsed" class="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Main</h3>
          <div class="mt-2 space-y-1">
            <router-link
              to="/"
              class="group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150"
              :class="$route.path === '/' ? 'bg-primary-100 text-primary-700' : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'"
              exact-active-class="bg-primary-100 text-primary-700"
            >
              <svg class="mr-3 flex-shrink-0 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7" />
                <rect x="14" y="3" width="7" height="7" />
                <rect x="14" y="14" width="7" height="7" />
                <rect x="3" y="14" width="7" height="7" />
              </svg>
              <span v-if="!isSidebarCollapsed">Dashboard</span>
            </router-link>

            <router-link
              to="/assets"
              class="group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150"
              :class="$route.path.startsWith('/assets') ? 'bg-primary-100 text-primary-700' : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'"
              active-class="bg-primary-100 text-primary-700"
            >
              <svg class="mr-3 flex-shrink-0 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                <line x1="8" y1="21" x2="16" y2="21" />
                <line x1="12" y1="17" x2="12" y2="21" />
              </svg>
              <span v-if="!isSidebarCollapsed">Assets</span>
            </router-link>

            <router-link
              to="/graph"
              class="group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150"
              :class="$route.path === '/graph' ? 'bg-primary-100 text-primary-700' : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'"
              active-class="bg-primary-100 text-primary-700"
            >
              <svg class="mr-3 flex-shrink-0 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <ellipse cx="12" cy="5" rx="9" ry="3" />
                <path d="m21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
              </svg>
              <span v-if="!isSidebarCollapsed">Dependency Graph</span>
            </router-link>

            <router-link
              to="/impact"
              class="group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150"
              :class="$route.path === '/impact' ? 'bg-primary-100 text-primary-700' : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'"
              active-class="bg-primary-100 text-primary-700"
            >
              <svg class="mr-3 flex-shrink-0 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="m22 2-7 20-4-9-9-4Z" />
                <path d="M22 2 11 13" />
              </svg>
              <span v-if="!isSidebarCollapsed">Impact Analysis</span>
            </router-link>
          </div>
        </div>

        <div>
          <h3 v-if="!isSidebarCollapsed" class="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Tools</h3>
          <div class="mt-2 space-y-1">
            <router-link
              to="/reports"
              class="group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150"
              :class="$route.path === '/reports' ? 'bg-primary-100 text-primary-700' : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'"
              active-class="bg-primary-100 text-primary-700"
            >
              <svg class="mr-3 flex-shrink-0 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14,2 14,8 20,8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <polyline points="10,9 9,9 8,9" />
              </svg>
              <span v-if="!isSidebarCollapsed">Reports</span>
            </router-link>

            <router-link
              to="/settings"
              class="group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150"
              :class="$route.path === '/settings' ? 'bg-primary-100 text-primary-700' : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'"
              active-class="bg-primary-100 text-primary-700"
            >
              <svg class="mr-3 flex-shrink-0 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3" />
                <path d="m12 1 1.09 3.26L16 5l-1.74 2.91L17 9l-3.26 1.09L13 13l-2.91-1.74L9 17l-1.09-3.26L5 13l1.74-2.91L4 7l3.26-1.09L8 3l2.91 1.74Z" />
              </svg>
              <span v-if="!isSidebarCollapsed">Settings</span>
            </router-link>
          </div>
        </div>
      </nav>

      <!-- User Section -->
      <div class="absolute bottom-0 w-full p-4 border-t border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
            </svg>
          </div>
          <div v-if="!isSidebarCollapsed" class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">Admin User</p>
            <p class="text-xs text-gray-500 truncate">Administrator</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="bg-white shadow-sm border-b border-gray-200">
        <div class="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
          <div class="flex items-center space-x-4">
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen"
              class="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="3" y1="6" x2="21" y2="6" />
                <line x1="3" y1="12" x2="21" y2="12" />
                <line x1="3" y1="18" x2="21" y2="18" />
              </svg>
            </button>

            <!-- Breadcrumbs -->
            <nav class="hidden sm:flex items-center space-x-2 text-sm">
              <router-link to="/" class="text-gray-500 hover:text-gray-700">Home</router-link>
              <template v-for="(crumb, index) in breadcrumbs" :key="index">
                <span class="text-gray-300">/</span>
                <router-link v-if="crumb.to" :to="crumb.to" class="text-gray-500 hover:text-gray-700">
                  {{ crumb.name }}
                </router-link>
                <span v-else class="text-gray-900 font-medium">{{ crumb.name }}</span>
              </template>
            </nav>
          </div>

          <div class="flex items-center space-x-4">
            <!-- Search -->
            <div class="relative max-w-xs w-full">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-4 w-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8" />
                  <path d="m21 21-4.35-4.35" />
                </svg>
              </div>
              <input 
                type="text" 
                placeholder="Search assets..." 
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 text-sm"
                v-model="searchQuery"
                @keydown.enter="handleSearch"
              />
            </div>

            <!-- Notifications -->
            <button class="p-2 text-gray-400 hover:text-gray-500">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
                <path d="M13.73 21a2 2 0 0 1-3.46 0" />
              </svg>
            </button>

            <!-- Profile -->
            <button class="p-2 text-gray-400 hover:text-gray-500">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <div class="flex-1 overflow-auto">
        <div class="p-4 sm:p-6 lg:p-8">
          <router-view />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isMobileMenuOpen = ref(false)
const isSidebarCollapsed = ref(false)
const searchQuery = ref('')

// Breadcrumbs computation
const breadcrumbs = computed(() => {
  const pathSegments = route.path.split('/').filter(segment => segment)
  return pathSegments.map((segment, index) => {
    const path = '/' + pathSegments.slice(0, index + 1).join('/')
    const isLast = index === pathSegments.length - 1
    return {
      name: segment.charAt(0).toUpperCase() + segment.slice(1),
      to: isLast ? null : path
    }
  })
})

// Search handler
const handleSearch = () => {
  console.log('Searching for:', searchQuery.value)
  // TODO: Implement search functionality
}
</script>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animation transitions */
.router-link-active {
  transition: all 0.2s ease-in-out;
}

/* Loading animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Gradient backgrounds */
.bg-gradient-constellation {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
}

/* Custom focus styles */
.focus-constellation:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
}

/* Card hover effects */
.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease-in-out;
}
</style>
