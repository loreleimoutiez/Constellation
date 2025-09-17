<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-constellation-800 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
              <router-link to="/" class="flex items-center">
                <svg class="h-8 w-8 text-constellation-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span class="ml-2 text-xl font-bold text-white">Constellation</span>
              </router-link>
            </div>
            
            <!-- Navigation Links -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="border-transparent text-gray-300 hover:border-constellation-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-constellation-300 text-white"
              >
                Dashboard
              </router-link>
              <router-link
                to="/cis"
                class="border-transparent text-gray-300 hover:border-constellation-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-constellation-300 text-white"
              >
                Assets
              </router-link>
              <router-link
                to="/graph"
                class="border-transparent text-gray-300 hover:border-constellation-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-constellation-300 text-white"
              >
                Graph View
              </router-link>
              <router-link
                to="/impact"
                class="border-transparent text-gray-300 hover:border-constellation-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-constellation-300 text-white"
              >
                Impact Analysis
              </router-link>
            </div>
          </div>

          <!-- Mobile menu button -->
          <div class="sm:hidden flex items-center">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-300 hover:text-white hover:bg-constellation-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-constellation-500"
            >
              <svg class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
                <path 
                  :class="{'hidden': mobileMenuOpen, 'inline-flex': !mobileMenuOpen }"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
                <path
                  :class="{'hidden': !mobileMenuOpen, 'inline-flex': mobileMenuOpen }"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile menu -->
      <div :class="{'block': mobileMenuOpen, 'hidden': !mobileMenuOpen}" class="sm:hidden">
        <div class="pt-2 pb-3 space-y-1">
          <router-link
            to="/"
            class="text-gray-300 hover:bg-constellation-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
            active-class="bg-constellation-700 text-white"
            @click="mobileMenuOpen = false"
          >
            Dashboard
          </router-link>
          <router-link
            to="/cis"
            class="text-gray-300 hover:bg-constellation-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
            active-class="bg-constellation-700 text-white"
            @click="mobileMenuOpen = false"
          >
            Assets
          </router-link>
          <router-link
            to="/graph"
            class="text-gray-300 hover:bg-constellation-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
            active-class="bg-constellation-700 text-white"
            @click="mobileMenuOpen = false"
          >
            Graph View
          </router-link>
          <router-link
            to="/impact"
            class="text-gray-300 hover:bg-constellation-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
            active-class="bg-constellation-700 text-white"
            @click="mobileMenuOpen = false"
          >
            Impact Analysis
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="py-10">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'

const mobileMenuOpen = ref(false)
</script>
