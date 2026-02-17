<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">🍽️ Meal Prep Selector</h1>
        <p class="text-gray-600">Select your proteins and get a randomized meal plan with recipes</p>
      </div>

      <!-- Main Content -->
      <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
        <ProteinSelector @generate="handleGenerate" :loading="loading" />
      </div>

      <!-- Recipe Display -->
      <RecipeDisplay 
        v-if="recipes.length > 0" 
        :recipes="recipes" 
      />

      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProteinSelector from './components/ProteinSelector.vue'
import RecipeDisplay from './components/RecipeDisplay.vue'

const recipes = ref([])
const loading = ref(false)
const error = ref(null)

const handleGenerate = async (selection) => {
  loading.value = true
  error.value = null
  recipes.value = []

  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(selection)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    recipes.value = data.recipes || []
    
    if (recipes.value.length === 0) {
      error.value = data.message || 'No recipes found'
    }
  } catch (err) {
    error.value = `Failed to fetch recipes: ${err.message}`
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>
