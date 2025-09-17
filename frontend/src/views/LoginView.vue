<template>
  <div class="min-h-screen bg-gradient-to-br from-constellation-900 via-constellation-800 to-constellation-700 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto h-20 w-20 bg-white rounded-2xl flex items-center justify-center shadow-2xl">
          <div class="h-12 w-12 bg-constellation-600 rounded-xl flex items-center justify-center">
            <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
        </div>
        <h2 class="mt-6 text-4xl font-bold text-white">
          Constellation
        </h2>
        <p class="mt-2 text-lg text-constellation-200">
          Configuration Management Database
        </p>
      </div>

      <!-- Login/Register Card -->
      <BaseCard class="bg-white/95 backdrop-blur-sm border-0 shadow-2xl">
        <div class="px-8 py-6">
          <!-- Toggle Buttons -->
          <div class="flex bg-gray-100 rounded-lg p-1 mb-6">
            <button
              @click="isLogin = true"
              :class="[
                'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-200',
                isLogin
                  ? 'bg-white text-constellation-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              Se connecter
            </button>
            <button
              @click="isLogin = false"
              :class="[
                'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-200',
                !isLogin
                  ? 'bg-white text-constellation-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              Créer un compte
            </button>
          </div>

          <!-- Login Form -->
          <form v-if="isLogin" @submit.prevent="handleLogin" class="space-y-6">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                Adresse e-mail
              </label>
              <BaseInput
                id="email"
                v-model="loginForm.email"
                type="email"
                required
                placeholder="votre.email@exemple.com"
                class="w-full"
              />
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                Mot de passe
              </label>
              <BaseInput
                id="password"
                v-model="loginForm.password"
                type="password"
                required
                placeholder="••••••••"
                class="w-full"
              />
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  v-model="loginForm.remember"
                  class="h-4 w-4 text-constellation-600 focus:ring-constellation-500 border-gray-300 rounded"
                >
                <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                  Se souvenir de moi
                </label>
              </div>

              <div class="text-sm">
                <a href="#" class="font-medium text-constellation-600 hover:text-constellation-500">
                  Mot de passe oublié ?
                </a>
              </div>
            </div>

            <BaseButton
              type="submit"
              variant="primary"
              size="lg"
              :loading="loading"
              class="w-full"
            >
              Se connecter
            </BaseButton>
          </form>

          <!-- Register Form -->
          <form v-else @submit.prevent="handleRegister" class="space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="firstName" class="block text-sm font-medium text-gray-700 mb-2">
                  Prénom
                </label>
                <BaseInput
                  id="firstName"
                  v-model="registerForm.firstName"
                  type="text"
                  required
                  placeholder="Jean"
                  class="w-full"
                />
              </div>
              <div>
                <label for="lastName" class="block text-sm font-medium text-gray-700 mb-2">
                  Nom
                </label>
                <BaseInput
                  id="lastName"
                  v-model="registerForm.lastName"
                  type="text"
                  required
                  placeholder="Dupont"
                  class="w-full"
                />
              </div>
            </div>

            <div>
              <label for="register-email" class="block text-sm font-medium text-gray-700 mb-2">
                Adresse e-mail
              </label>
              <BaseInput
                id="register-email"
                v-model="registerForm.email"
                type="email"
                required
                placeholder="votre.email@exemple.com"
                class="w-full"
              />
            </div>

            <div>
              <label for="register-password" class="block text-sm font-medium text-gray-700 mb-2">
                Mot de passe
              </label>
              <BaseInput
                id="register-password"
                v-model="registerForm.password"
                type="password"
                required
                placeholder="••••••••"
                class="w-full"
              />
            </div>

            <div>
              <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
                Confirmer le mot de passe
              </label>
              <BaseInput
                id="confirm-password"
                v-model="registerForm.confirmPassword"
                type="password"
                required
                placeholder="••••••••"
                class="w-full"
              />
            </div>

            <div class="flex items-center">
              <input
                id="terms"
                name="terms"
                type="checkbox"
                v-model="registerForm.acceptTerms"
                required
                class="h-4 w-4 text-constellation-600 focus:ring-constellation-500 border-gray-300 rounded"
              >
              <label for="terms" class="ml-2 block text-sm text-gray-700">
                J'accepte les 
                <a href="#" class="font-medium text-constellation-600 hover:text-constellation-500">
                  conditions d'utilisation
                </a>
                et la 
                <a href="#" class="font-medium text-constellation-600 hover:text-constellation-500">
                  politique de confidentialité
                </a>
              </label>
            </div>

            <BaseButton
              type="submit"
              variant="primary"
              size="lg"
              :loading="loading"
              class="w-full"
            >
              Créer un compte
            </BaseButton>
          </form>

          <!-- Error Message -->
          <div v-if="errorMessage" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p class="text-sm text-red-600">{{ errorMessage }}</p>
          </div>
        </div>
      </BaseCard>

      <!-- Footer -->
      <div class="text-center">
        <p class="text-constellation-300 text-sm">
          © 2025 Constellation CMDB. Tous droits réservés.
        </p>
        <div class="mt-2 flex justify-center space-x-4 text-constellation-400 text-sm">
          <a href="#" class="hover:text-constellation-200 transition-colors">Documentation</a>
          <a href="#" class="hover:text-constellation-200 transition-colors">Support</a>
          <a href="#" class="hover:text-constellation-200 transition-colors">API</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const isLogin = ref(true)
const loading = ref(false)
const errorMessage = ref('')

// Login form
const loginForm = ref({
  email: '',
  password: '',
  remember: false,
})

// Register form
const registerForm = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
})

const handleLogin = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    
    // TODO: Implement actual authentication with backend
    console.log('Login attempt:', loginForm.value)
    
    // Simulated delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // For now, just redirect to dashboard
    await router.push('/dashboard')
    
  } catch (error) {
    errorMessage.value = 'Erreur de connexion. Veuillez vérifier vos identifiants.'
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    
    // Validate password confirmation
    if (registerForm.value.password !== registerForm.value.confirmPassword) {
      errorMessage.value = 'Les mots de passe ne correspondent pas.'
      return
    }
    
    // TODO: Implement actual registration with backend
    console.log('Register attempt:', registerForm.value)
    
    // Simulated delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // For now, just switch to login
    isLogin.value = true
    
  } catch (error) {
    errorMessage.value = 'Erreur lors de la création du compte. Veuillez réessayer.'
    console.error('Register error:', error)
  } finally {
    loading.value = false
  }
}
</script>