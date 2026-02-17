<template>
  <div class="protein-selector">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Select Protein Quantities</h2>
    <p class="text-gray-600 mb-6">Choose how many meals you want for each protein type</p>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
      <!-- Chicken -->
      <div class="protein-item">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          🐔 Chicken
        </label>
        <input 
          v-model.number="selection.chicken"
          type="number" 
          min="0" 
          max="10"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="0"
        />
      </div>

      <!-- Beef -->
      <div class="protein-item">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          🥩 Beef
        </label>
        <input 
          v-model.number="selection.beef"
          type="number" 
          min="0" 
          max="10"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="0"
        />
      </div>

      <!-- Pork -->
      <div class="protein-item">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          🐷 Pork
        </label>
        <input 
          v-model.number="selection.pork"
          type="number" 
          min="0" 
          max="10"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="0"
        />
      </div>

      <!-- Fish -->
      <div class="protein-item">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          🐟 Fish
        </label>
        <input 
          v-model.number="selection.fish"
          type="number" 
          min="0" 
          max="10"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="0"
        />
      </div>

      <!-- Vegetarian -->
      <div class="protein-item">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          🥗 Vegetarian
        </label>
        <input 
          v-model.number="selection.vegetarian"
          type="number" 
          min="0" 
          max="10"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="0"
        />
      </div>
    </div>

    <!-- Generate Button -->
    <div class="text-center">
      <button 
        @click="generateMealPlan"
        :disabled="loading || totalSelected === 0"
        class="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition duration-200"
      >
        <span v-if="loading">
          <svg class="animate-spin inline-block h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Generating...
        </span>
        <span v-else>
          Generate Meal Plan ({{ totalSelected }} meals)
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['generate'])

const selection = ref({
  chicken: 0,
  beef: 0,
  pork: 0,
  fish: 0,
  vegetarian: 0
})

const totalSelected = computed(() => {
  return Object.values(selection.value).reduce((sum, val) => sum + val, 0)
})

const generateMealPlan = () => {
  if (totalSelected.value > 0) {
    emit('generate', selection.value)
  }
}
</script>
