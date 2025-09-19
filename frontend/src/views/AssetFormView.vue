<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">
                {{ isEditing ? 'Edit Asset' : 'Create Asset' }}
              </h1>
              <p class="mt-2 text-gray-600">
                {{ isEditing ? 'Update asset information' : 'Add a new configuration item to your CMDB' }}
              </p>
            </div>
            <BaseButton variant="secondary" @click="$router.push('/assets')">
              Cancel
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Form -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Basic Information -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Basic Information</h2>
            </template>
            
            <div class="space-y-6">
              <!-- Asset Category Selection -->
              <div>
                <label for="category" class="block text-sm font-medium text-gray-700">Asset Category *</label>
                <select
                  id="category"
                  v-model="form.category"
                  required
                  @change="onCategoryChange"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                  :class="{ 'border-red-500': errors.category }"
                >
                  <option value="">Select category</option>
                  <option value="tangible">Tangible (Physical/Technical Assets)</option>
                  <option value="intangible">Intangible (People, Policies, Processes, Virtual Assets)</option>
                </select>
                <p v-if="errors.category" class="mt-1 text-sm text-red-600">{{ errors.category }}</p>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="name" class="block text-sm font-medium text-gray-700">Name *</label>
                  <BaseInput
                    id="name"
                    v-model="form.name"
                    placeholder="Enter asset name"
                    required
                    :error="errors.name"
                  />
                </div>
                
                <div>
                  <label for="ci_type" class="block text-sm font-medium text-gray-700">
                    {{ form.category === 'intangible' ? 'Intangible Type' : 'Type' }} *
                  </label>
                  <select
                    id="ci_type"
                    v-model="form.ci_type"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                    :class="{ 'border-red-500': errors.ci_type }"
                  >
                    <option value="">{{ form.category === 'intangible' ? 'Select intangible type' : 'Select type' }}</option>
                    
                    <!-- Tangible Asset Types -->
                    <template v-if="form.category === 'tangible'">
                      <option value="APPLICATION">Application</option>
                      <option value="DATABASE">Database</option>
                      <option value="HARDWARE">Hardware</option>
                      <option value="NETWORK">Network</option>
                      <option value="SERVICE">Service</option>
                      <option value="STORAGE">Storage</option>
                      <option value="GENERIC">Generic</option>
                    </template>
                    
                    <!-- Intangible Asset Types -->
                    <template v-else-if="form.category === 'intangible'">
                      <optgroup label="Human Resources">
                        <option value="human">Person</option>
                        <option value="team">Team</option>
                        <option value="role">Role</option>
                      </optgroup>
                      <optgroup label="Governance">
                        <option value="policy">Policy</option>
                        <option value="procedure">Procedure</option>
                        <option value="standard">Standard</option>
                      </optgroup>
                      <optgroup label="Legal/Contractual">
                        <option value="license">License</option>
                        <option value="contract">Contract</option>
                        <option value="sla">SLA</option>
                      </optgroup>
                      <optgroup label="Business Processes">
                        <option value="process">Process</option>
                        <option value="workflow">Workflow</option>
                      </optgroup>
                      <optgroup label="Knowledge">
                        <option value="knowledge">Knowledge</option>
                        <option value="documentation">Documentation</option>
                      </optgroup>
                      <optgroup label="Virtual/Logical Assets">
                        <option value="virtual_machine">Virtual Machine</option>
                        <option value="container">Container</option>
                        <option value="software">Software</option>
                        <option value="api">API</option>
                        <option value="microservice">Microservice</option>
                      </optgroup>
                    </template>
                  </select>
                  <p v-if="errors.ci_type" class="mt-1 text-sm text-red-600">{{ errors.ci_type }}</p>
                </div>
              </div>

              <div>
                <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  id="description"
                  v-model="form.description"
                  rows="3"
                  placeholder="Describe this asset..."
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                ></textarea>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label for="criticality" class="block text-sm font-medium text-gray-700">Criticality *</label>
                  <select
                    id="criticality"
                    v-model="form.criticality"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                  >
                    <option value="LOW">Low</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="HIGH">High</option>
                    <option value="CRITICAL">Critical</option>
                  </select>
                </div>

                <!-- Environment et Lifecycle State uniquement pour les assets tangibles -->
                <div v-if="form.category === 'tangible'">
                  <label for="environment" class="block text-sm font-medium text-gray-700">Environment *</label>
                  <select
                    id="environment"
                    v-model="form.environment"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                  >
                    <option value="DEV">Development</option>
                    <option value="TEST">Test</option>
                    <option value="STAGING">Staging</option>
                    <option value="PROD">Production</option>
                  </select>
                </div>

                <div v-if="form.category === 'tangible'">
                  <label for="lifecycle_state" class="block text-sm font-medium text-gray-700">Lifecycle State</label>
                  <select
                    id="lifecycle_state"
                    v-model="form.lifecycle_state"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                  >
                    <option value="PLANNED">Planned</option>
                    <option value="ACTIVE">Active</option>
                    <option value="DEPRECATED">Deprecated</option>
                    <option value="RETIRED">Retired</option>
                  </select>
                </div>
              </div>
            </div>
          </BaseCard>

          <!-- Technical Information (Tangible Assets Only) -->
          <BaseCard v-if="form.category === 'tangible'">
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Technical Information</h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="hostname" class="block text-sm font-medium text-gray-700">Hostname</label>
                <BaseInput
                  id="hostname"
                  v-model="form.hostname"
                  placeholder="server01.domain.com"
                />
              </div>

              <div>
                <label for="ip_address" class="block text-sm font-medium text-gray-700">IP Address</label>
                <BaseInput
                  id="ip_address"
                  v-model="form.ip_address"
                  placeholder="192.168.1.100"
                />
              </div>

              <div>
                <label for="fqdn" class="block text-sm font-medium text-gray-700">FQDN</label>
                <BaseInput
                  id="fqdn"
                  v-model="form.fqdn"
                  placeholder="server01.production.company.com"
                />
              </div>

              <div>
                <label for="vendor" class="block text-sm font-medium text-gray-700">Vendor</label>
                <BaseInput
                  id="vendor"
                  v-model="form.vendor"
                  placeholder="Dell, HP, Cisco..."
                />
              </div>

              <div>
                <label for="model" class="block text-sm font-medium text-gray-700">Model</label>
                <BaseInput
                  id="model"
                  v-model="form.model"
                  placeholder="PowerEdge R740, ProLiant DL380..."
                />
              </div>

              <div>
                <label for="location" class="block text-sm font-medium text-gray-700">Location</label>
                <BaseInput
                  id="location"
                  v-model="form.location"
                  placeholder="Datacenter A, Rack 15, Unit 12"
                />
              </div>
            </div>
          </BaseCard>

          <!-- Human Resources Information (Human Assets) -->
          <BaseCard v-if="form.category === 'intangible' && ['human', 'team', 'role'].includes(form.ci_type)">
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">
                {{ form.ci_type === 'human' ? 'Personal Information' : form.ci_type === 'team' ? 'Team Information' : 'Role Information' }}
              </h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-if="form.ci_type === 'human'">
                <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                <BaseInput
                  id="email"
                  v-model="form.human_attributes.email"
                  type="email"
                  placeholder="john.doe@company.com"
                />
              </div>

              <div>
                <label for="department" class="block text-sm font-medium text-gray-700">Department</label>
                <BaseInput
                  id="department"
                  v-model="form.human_attributes.department"
                  placeholder="IT, HR, Finance..."
                />
              </div>

              <div v-if="form.ci_type === 'human'">
                <label for="job_title" class="block text-sm font-medium text-gray-700">Job Title</label>
                <BaseInput
                  id="job_title"
                  v-model="form.human_attributes.job_title"
                  placeholder="Senior Developer, System Administrator..."
                />
              </div>

              <div v-if="form.ci_type === 'human'">
                <label for="manager" class="block text-sm font-medium text-gray-700">Manager</label>
                <BaseInput
                  id="manager"
                  v-model="form.human_attributes.manager"
                  placeholder="Manager name or ID"
                />
              </div>

              <div v-if="form.ci_type === 'human'">
                <label for="phone" class="block text-sm font-medium text-gray-700">Phone</label>
                <BaseInput
                  id="phone"
                  v-model="form.human_attributes.phone"
                  placeholder="+1 (555) 123-4567"
                />
              </div>

              <div v-if="form.ci_type === 'human'">
                <label for="employee_id" class="block text-sm font-medium text-gray-700">Employee ID</label>
                <BaseInput
                  id="employee_id"
                  v-model="form.human_attributes.employee_id"
                  placeholder="EMP001234"
                />
              </div>
            </div>
          </BaseCard>

          <!-- Policy/Governance Information -->
          <BaseCard v-if="form.category === 'intangible' && ['policy', 'procedure', 'standard'].includes(form.ci_type)">
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Governance Information</h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="policy_type" class="block text-sm font-medium text-gray-700">Policy Type</label>
                <select
                  id="policy_type"
                  v-model="form.policy_attributes.policy_type"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                >
                  <option value="security">Security</option>
                  <option value="compliance">Compliance</option>
                  <option value="operational">Operational</option>
                  <option value="hr">Human Resources</option>
                </select>
              </div>

              <div>
                <label for="approval_status" class="block text-sm font-medium text-gray-700">Approval Status</label>
                <select
                  id="approval_status"
                  v-model="form.policy_attributes.approval_status"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                >
                  <option value="draft">Draft</option>
                  <option value="under_review">Under Review</option>
                  <option value="approved">Approved</option>
                  <option value="deprecated">Deprecated</option>
                </select>
              </div>

              <div>
                <label for="owner_department" class="block text-sm font-medium text-gray-700">Owner Department</label>
                <BaseInput
                  id="owner_department"
                  v-model="form.policy_attributes.owner_department"
                  placeholder="IT Security, Legal, HR..."
                />
              </div>

              <div>
                <label for="approval_date" class="block text-sm font-medium text-gray-700">Approval Date</label>
                <BaseInput
                  id="approval_date"
                  v-model="form.policy_attributes.approval_date"
                  type="text"
                  placeholder="YYYY-MM-DD"
                />
              </div>

              <div>
                <label for="review_date" class="block text-sm font-medium text-gray-700">Next Review Date</label>
                <BaseInput
                  id="review_date"
                  v-model="form.policy_attributes.review_date"
                  type="text"
                  placeholder="YYYY-MM-DD"
                />
              </div>
            </div>
          </BaseCard>

          <!-- License Information -->
          <BaseCard v-if="form.category === 'intangible' && ['license', 'contract', 'sla'].includes(form.ci_type)">
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">
                {{ form.ci_type === 'license' ? 'License Information' : form.ci_type === 'contract' ? 'Contract Information' : 'SLA Information' }}
              </h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-if="form.ci_type === 'license'">
                <label for="license_type" class="block text-sm font-medium text-gray-700">License Type</label>
                <BaseInput
                  id="license_type"
                  v-model="form.license_attributes.license_type"
                  placeholder="Per-user, Site license, Enterprise..."
                />
              </div>

              <div>
                <label for="vendor" class="block text-sm font-medium text-gray-700">Vendor</label>
                <BaseInput
                  id="vendor"
                  v-model="form.license_attributes.vendor"
                  placeholder="Microsoft, Oracle, Adobe..."
                />
              </div>

              <div v-if="form.ci_type === 'license'" class="md:col-span-2">
                <label for="license_key" class="block text-sm font-medium text-gray-700">License Key</label>
                <BaseInput
                  id="license_key"
                  v-model="form.license_attributes.license_key"
                  placeholder="XXXXX-XXXXX-XXXXX-XXXXX"
                  type="password"
                />
              </div>

              <div v-if="form.ci_type === 'license'">
                <label for="seats_total" class="block text-sm font-medium text-gray-700">Total Seats</label>
                <BaseInput
                  id="seats_total"
                  v-model.number="form.license_attributes.seats_total"
                  type="number"
                  placeholder="100"
                />
              </div>

              <div v-if="form.ci_type === 'license'">
                <label for="seats_used" class="block text-sm font-medium text-gray-700">Used Seats</label>
                <BaseInput
                  id="seats_used"
                  v-model.number="form.license_attributes.seats_used"
                  type="number"
                  placeholder="85"
                />
              </div>

              <div v-if="form.ci_type === 'license'">
                <label for="cost_per_seat" class="block text-sm font-medium text-gray-700">Cost per Seat</label>
                <BaseInput
                  id="cost_per_seat"
                  v-model.number="form.license_attributes.cost_per_seat"
                  type="number"
                  step="0.01"
                  placeholder="25.00"
                />
              </div>

              <div>
                <label for="renewal_date" class="block text-sm font-medium text-gray-700">
                  {{ form.ci_type === 'license' ? 'Renewal Date' : 'Expiration Date' }}
                </label>
                <BaseInput
                  id="renewal_date"
                  v-model="form.license_attributes.renewal_date"
                  type="text"
                  placeholder="YYYY-MM-DD"
                />
              </div>

              <div v-if="form.ci_type === 'license'">
                <label for="support_level" class="block text-sm font-medium text-gray-700">Support Level</label>
                <select
                  id="support_level"
                  v-model="form.license_attributes.support_level"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                >
                  <option value="">Select support level</option>
                  <option value="basic">Basic</option>
                  <option value="standard">Standard</option>
                  <option value="premium">Premium</option>
                  <option value="enterprise">Enterprise</option>
                </select>
              </div>
            </div>
          </BaseCard>

          <!-- Technical Information (Tangible Assets Only) -->
          <BaseCard v-if="form.category === 'tangible'">
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Technical Information</h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="vendor" class="block text-sm font-medium text-gray-700">Vendor</label>
                <BaseInput
                  id="vendor"
                  v-model="form.vendor"
                  placeholder="Dell, HP, Cisco..."
                />
              </div>

              <div>
                <label for="model" class="block text-sm font-medium text-gray-700">Model</label>
                <BaseInput
                  id="model"
                  v-model="form.model"
                  placeholder="PowerEdge R750, ProLiant DL380..."
                />
              </div>

              <div>
                <label for="location" class="block text-sm font-medium text-gray-700">Location</label>
                <BaseInput
                  id="location"
                  v-model="form.location"
                  placeholder="DataCenter-A-Rack-05"
                />
              </div>
            </div>
          </BaseCard>

          <!-- Operational Flags (Tangible Assets Only) -->
          <BaseCard v-if="form.category === 'tangible'">
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Operational Settings</h2>
            </template>
            
            <div class="space-y-4">
              <div class="flex items-center">
                <input
                  id="monitoring_enabled"
                  v-model="form.monitoring_enabled"
                  type="checkbox"
                  class="h-4 w-4 text-constellation-600 focus:ring-constellation-500 border-gray-300 rounded"
                />
                <label for="monitoring_enabled" class="ml-2 block text-sm text-gray-900">
                  Enable monitoring for this asset
                </label>
              </div>

              <div class="flex items-center">
                <input
                  id="backup_enabled"
                  v-model="form.backup_enabled"
                  type="checkbox"
                  class="h-4 w-4 text-constellation-600 focus:ring-constellation-500 border-gray-300 rounded"
                />
                <label for="backup_enabled" class="ml-2 block text-sm text-gray-900">
                  Enable backup for this asset
                </label>
              </div>
            </div>
          </BaseCard>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Preview -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Preview</h2>
            </template>
            
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <component :is="getAssetIcon(form.ci_type)" class="h-6 w-6 text-constellation-600" />
                <div>
                  <p class="font-medium text-gray-900">{{ form.name || 'Asset Name' }}</p>
                  <p class="text-sm text-gray-500">{{ form.ci_type || 'TYPE' }}</p>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Criticality:</span>
                <span
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    getCriticalityClasses(form.criticality)
                  ]"
                >
                  {{ form.criticality || 'MEDIUM' }}
                </span>
              </div>

              <!-- Environment et State uniquement pour les assets tangibles -->
              <div v-if="form.category === 'tangible'" class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Environment:</span>
                <span class="text-sm font-medium">{{ form.environment || 'PROD' }}</span>
              </div>

              <div v-if="form.category === 'tangible'" class="flex items-center justify-between">
                <span class="text-sm text-gray-600">State:</span>
                <div class="flex items-center space-x-2">
                  <div
                    :class="[
                      'h-2 w-2 rounded-full',
                      form.lifecycle_state === 'ACTIVE' ? 'bg-green-500' :
                      form.lifecycle_state === 'PLANNED' ? 'bg-blue-500' : 
                      form.lifecycle_state === 'DEPRECATED' ? 'bg-yellow-500' : 'bg-gray-500'
                    ]"
                  ></div>
                  <span class="text-sm">{{ form.lifecycle_state || 'ACTIVE' }}</span>
                </div>
              </div>
            </div>
          </BaseCard>

          <!-- Relations -->
          <BaseCard>
            <template #header>
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                  </svg>
                  <h2 class="text-lg font-semibold text-gray-900">Asset Relations</h2>
                </div>
                <span v-if="!isEditing" class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full font-medium">Creation Mode</span>
                <span v-else class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">Edit Mode</span>
              </div>
            </template>
            
            <RelationshipManager 
              v-if="isEditing && route.params.id"
              :asset-id="route.params.id as string" 
            />
            
            <RelationshipCreator 
              v-else
              v-model="selectedRelationships"
              :exclude-ci-id="null"
            />
          </BaseCard>

          <!-- Actions -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Actions</h2>
            </template>
            
            <div class="space-y-3">
              <BaseButton
                type="submit"
                :variant="buttonVariant"
                :loading="loading"
                :disabled="!isFormValid"
                class="w-full"
              >
                {{ buttonText }}
              </BaseButton>
              
              <BaseButton
                variant="secondary"
                type="button"
                class="w-full"
                @click="resetForm"
              >
                Reset Form
              </BaseButton>

              <BaseButton
                variant="outline"
                type="button"
                class="w-full"
                @click="$router.push('/assets')"
              >
                Cancel
              </BaseButton>
            </div>
          </BaseCard>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCMDBStore } from '@/stores/cmdb'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import RelationshipManager from '@/components/RelationshipManager.vue'
import RelationshipCreator from '@/components/RelationshipCreator.vue'
import {
  ServerIcon,
  ComputerDesktopIcon,
  CpuChipIcon,
  CloudIcon,
  GlobeAltIcon,
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const cmdbStore = useCMDBStore()

// Reactive data
const loading = ref(false)
const errors = ref<Record<string, string>>({})

// Check if we're in edit mode
const isEditing = computed(() => route.params.id !== undefined)

// Form data
const form = ref({
  name: '',
  description: '',
  category: 'tangible',
  ci_type: '',
  intangible_type: '',
  criticality: 'MEDIUM',
  environment: 'PROD',
  lifecycle_state: 'ACTIVE',
  hostname: '',
  ip_address: '',
  fqdn: '',
  vendor: '',
  model: '',
  location: '',
  monitoring_enabled: true,
  backup_enabled: false,
  // Intangible asset specific fields
  human_attributes: {
    email: '',
    department: '',
    job_title: '',
    manager: '',
    skills: [] as string[],
    certifications: [] as string[],
    phone: '',
    employee_id: ''
  },
  policy_attributes: {
    policy_type: 'security',
    approval_status: 'draft',
    approval_date: '',
    review_date: '',
    owner_department: '',
    compliance_frameworks: [] as string[]
  },
  license_attributes: {
    license_type: '',
    vendor: '',
    license_key: '',
    seats_total: 0,
    seats_used: 0,
    cost_per_seat: 0,
    renewal_date: '',
    support_level: ''
  }
})

// Relationships for creation mode
const selectedRelationships = ref<Array<{
  target_ci_id: string
  relationship_type: string
  description?: string
}>>([])

// Computed
const isFormValid = computed(() => {
  const basicFields = !!(form.value.name.trim() && form.value.criticality)
  
  // Pour tous les types d'assets, on vérifie ci_type
  const typeField = !!form.value.ci_type
  
  // Pour les assets tangibles, environment est aussi requis
  if (form.value.category === 'tangible') {
    return basicFields && typeField && form.value.environment
  }
  
  // Pour les assets intangibles, pas besoin d'environment
  return basicFields && typeField
})

const buttonText = computed(() => {
  if (loading.value) {
    return isEditing.value ? 'Updating...' : 'Creating...'
  }
  return isEditing.value ? 'Update Asset' : 'Create Asset'
})

const buttonVariant = computed(() => {
  if (loading.value) return 'secondary'
  return isFormValid.value ? 'success' : 'secondary'
})

// Methods
const getCategoryFromCiType = (ci_type: string): 'tangible' | 'intangible' => {
  // Tangible CI types (physical/technical assets)
  const tangibleTypes = [
    'APPLICATION', 'DATABASE', 'HARDWARE', 'NETWORK', 
    'SERVICE', 'STORAGE', 'GENERIC'
  ]
  
  if (tangibleTypes.includes(ci_type)) {
    return 'tangible'
  }
  
  // Everything else is considered intangible
  return 'intangible'
}

const onCategoryChange = () => {
  // Reset ci_type when category changes
  form.value.ci_type = ''
  form.value.intangible_type = ''
  
  // Set appropriate defaults based on category
  if (form.value.category === 'intangible') {
    // Pour les assets intangibles, on retire environment et lifecycle_state
    form.value.environment = ''
    form.value.lifecycle_state = ''
    form.value.monitoring_enabled = false
    form.value.backup_enabled = false
  } else {
    // Pour les assets tangibles, on garde les valeurs par défaut
    form.value.environment = 'PROD'
    form.value.lifecycle_state = 'ACTIVE'
    form.value.monitoring_enabled = true
    form.value.backup_enabled = false
  }
}

const getAssetIcon = (type: string) => {
  const iconMap: Record<string, any> = {
    APPLICATION: ComputerDesktopIcon,
    DATABASE: ServerIcon,
    HARDWARE: CpuChipIcon,
    NETWORK: GlobeAltIcon,
    SERVICE: CloudIcon,
    STORAGE: ServerIcon,
    GENERIC: ServerIcon,
  }
  return iconMap[type] || ServerIcon
}

const getCriticalityClasses = (criticality: string) => {
  const classMap: Record<string, string> = {
    CRITICAL: 'bg-red-100 text-red-800',
    HIGH: 'bg-orange-100 text-orange-800',
    MEDIUM: 'bg-yellow-100 text-yellow-800',
    LOW: 'bg-green-100 text-green-800',
  }
  return classMap[criticality] || 'bg-gray-100 text-gray-800'
}

const validateForm = () => {
  errors.value = {}

  if (!form.value.name.trim()) {
    errors.value.name = 'Name is required'
  }

  if (!form.value.category) {
    errors.value.category = 'Category is required'
  }

  if (!form.value.ci_type) {
    errors.value.ci_type = form.value.category === 'intangible' ? 'Intangible type is required' : 'Type is required'
  }

  return Object.keys(errors.value).length === 0
}

const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    category: 'tangible',
    ci_type: '',
    intangible_type: '',
    criticality: 'MEDIUM',
    environment: 'PROD',  // Sera ajusté par updateFormDefaults si intangible
    lifecycle_state: 'ACTIVE',  // Sera ajusté par updateFormDefaults si intangible
    hostname: '',
    ip_address: '',
    fqdn: '',
    vendor: '',
    model: '',
    location: '',
    monitoring_enabled: true,
    backup_enabled: false,
    // Intangible asset specific fields
    human_attributes: {
      email: '',
      department: '',
      job_title: '',
      manager: '',
      skills: [] as string[],
      certifications: [] as string[],
      phone: '',
      employee_id: ''
    },
    policy_attributes: {
      policy_type: 'security',
      approval_status: 'draft',
      approval_date: '',
      review_date: '',
      owner_department: '',
      compliance_frameworks: [] as string[]
    },
    license_attributes: {
      license_type: '',
      vendor: '',
      license_key: '',
      seats_total: 0,
      seats_used: 0,
      cost_per_seat: 0,
      renewal_date: '',
      support_level: ''
    }
  }
  errors.value = {}
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    // Prepare data based on category
    let cleanedForm: any = { ...form.value }
    
    // Pour les assets intangibles, on ajuste la structure des données
    if (form.value.category === 'intangible') {
      // Exclure environment et lifecycle_state pour les assets intangibles
      // Le backend utilisera ses valeurs par défaut
      const { environment, lifecycle_state, ...intangibleForm } = cleanedForm
      cleanedForm = intangibleForm
      
      // Ajouter environment et lifecycle_state avec des valeurs par défaut pour intangible
      cleanedForm.environment = 'PROD'  // Valeur par défaut
      cleanedForm.lifecycle_state = 'ACTIVE'  // Valeur par défaut
      
      // Mapper les types intangibles vers les types backend valides
      const intangibleTypeMapping: Record<string, string> = {
        'human': 'IDENTITY',
        'team': 'IDENTITY', 
        'role': 'IDENTITY',
        'policy': 'GENERIC',
        'procedure': 'GENERIC',
        'standard': 'GENERIC',
        'license': 'SOFTWARE',
        'contract': 'GENERIC',
        'sla': 'GENERIC',
        'process': 'SERVICE',
        'workflow': 'SERVICE',
        'knowledge': 'DATASET',
        'documentation': 'DATASET',
        'virtual_machine': 'HARDWARE',
        'container': 'SOFTWARE',
        'software': 'SOFTWARE',
        'api': 'SERVICE',
        'microservice': 'SERVICE'
      }
      
      // Stocker le type original et mapper vers le type backend
      const originalType = cleanedForm.ci_type
      if (originalType && intangibleTypeMapping[originalType]) {
        cleanedForm.ci_type = intangibleTypeMapping[originalType]
      } else {
        cleanedForm.ci_type = 'GENERIC'
      }
      
      // Initialiser custom_attributes s'il n'existe pas
      if (!cleanedForm.custom_attributes) {
        cleanedForm.custom_attributes = {}
      }
      
      // Stocker le type original pour référence future
      cleanedForm.custom_attributes = {
        ...cleanedForm.custom_attributes,
        original_intangible_type: originalType,
        is_intangible_asset: true
      }
    } else {
      // Pour les assets tangibles, supprimer intangible_type
      const { intangible_type, ...tangibleForm } = cleanedForm
      cleanedForm = tangibleForm
    }
    
    // Clean up empty strings and null values
    cleanedForm = Object.fromEntries(
      Object.entries(cleanedForm).filter(([_, value]) => value !== '' && value !== null)
    )

    if (isEditing.value) {
      // Update existing asset
      await cmdbStore.updateCI(route.params.id as string, cleanedForm)
    } else {
      // Create new asset with relationships
      if (selectedRelationships.value.length > 0) {
        // Use the new endpoint for creating with relationships
        cleanedForm.relationships = selectedRelationships.value
        await cmdbStore.createCIWithRelationships(cleanedForm)
      } else {
        // Use the regular endpoint for basic creation
        await cmdbStore.createCI(cleanedForm)
      }
    }

    // Redirect to assets list
    router.push('/assets')
  } catch (error: any) {
    // Debug: Log the full error
    console.error('Asset creation error:', error)
    console.error('Error response:', error.response?.data)
    
    // Show user-friendly error message
    let errorMessage = 'Failed to save asset. Please try again.'
    if (error.response?.data?.detail) {
      errorMessage = `Validation error: ${JSON.stringify(error.response.data.detail)}`
    } else if (error.response?.data) {
      errorMessage = `Error: ${JSON.stringify(error.response.data)}`
    } else if (error.message) {
      errorMessage = `Error: ${error.message}`
    }
    
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

const loadAssetForEditing = async () => {
  if (!isEditing.value) return

  const assetId = route.params.id as string
  loading.value = true

  try {
    await cmdbStore.fetchCIs()
    const asset = cmdbStore.cis.find(ci => ci.id === assetId)
    
    if (asset) {
      // Deduce category from ci_type
      const deducedCategory = getCategoryFromCiType(asset.ci_type || '')
      
      // Populate form with existing asset data
      form.value = {
        name: asset.name || '',
        description: asset.description || '',
        category: asset.category || deducedCategory,  // Use existing category or deduce from ci_type
        ci_type: asset.ci_type || '',
        intangible_type: asset.intangible_type || '',
        criticality: asset.criticality || 'MEDIUM',
        environment: asset.environment || 'PROD',
        lifecycle_state: asset.lifecycle_state || 'ACTIVE',
        hostname: asset.hostname || '',
        ip_address: asset.ip_address || '',
        fqdn: asset.fqdn || '',
        vendor: asset.vendor || '',
        model: asset.model || '',
        location: asset.location || '',
        monitoring_enabled: asset.monitoring_enabled ?? true,
        backup_enabled: asset.backup_enabled ?? false,
        // Intangible asset specific fields
        human_attributes: {
          email: asset.human_attributes?.email || '',
          department: asset.human_attributes?.department || '',
          job_title: asset.human_attributes?.job_title || '',
          manager: asset.human_attributes?.manager || '',
          skills: asset.human_attributes?.skills || [],
          certifications: asset.human_attributes?.certifications || [],
          phone: asset.human_attributes?.phone || '',
          employee_id: asset.human_attributes?.employee_id || ''
        },
        policy_attributes: {
          policy_type: asset.policy_attributes?.policy_type || 'security',
          approval_status: asset.policy_attributes?.approval_status || 'draft',
          approval_date: asset.policy_attributes?.approval_date || '',
          review_date: asset.policy_attributes?.review_date || '',
          owner_department: asset.policy_attributes?.owner_department || '',
          compliance_frameworks: asset.policy_attributes?.compliance_frameworks || []
        },
        license_attributes: {
          license_type: asset.license_attributes?.license_type || '',
          vendor: asset.license_attributes?.vendor || '',
          license_key: asset.license_attributes?.license_key || '',
          seats_total: asset.license_attributes?.seats_total || 0,
          seats_used: asset.license_attributes?.seats_used || 0,
          cost_per_seat: asset.license_attributes?.cost_per_seat || 0,
          renewal_date: asset.license_attributes?.renewal_date || '',
          support_level: asset.license_attributes?.support_level || ''
        }
      }
    } else {
      // Asset not found
      router.push('/assets')
    }
  } catch (error) {
    console.error('Failed to load asset for editing:', error)
    router.push('/assets')
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  if (isEditing.value) {
    loadAssetForEditing()
  }
})
</script>