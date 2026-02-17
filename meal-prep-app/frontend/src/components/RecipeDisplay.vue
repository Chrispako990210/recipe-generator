<template>
  <div class="recipe-display">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6">
      Your Meal Plan ({{ recipes.length }} recipes)
    </h2>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div 
        v-for="(recipe, index) in recipes" 
        :key="index"
        class="recipe-card bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-200"
      >
        <!-- Recipe Image -->
        <div v-if="recipe.image" class="h-48 bg-gray-200 overflow-hidden">
          <img 
            :src="recipe.image" 
            :alt="recipe.title"
            class="w-full h-full object-cover"
            @error="handleImageError"
          />
        </div>
        <div v-else class="h-48 bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center">
          <span class="text-4xl">🍽️</span>
        </div>

        <!-- Recipe Content -->
        <div class="p-6">
          <!-- Title -->
          <h3 class="text-xl font-bold text-gray-800 mb-2">
            {{ recipe.title }}
          </h3>

          <!-- Servings -->
          <p class="text-sm text-gray-600 mb-4">
            Servings: {{ recipe.servings }}
          </p>

          <!-- Ingredients -->
          <div class="mb-4">
            <h4 class="font-semibold text-gray-700 mb-2">Ingredients:</h4>
            <ul class="list-disc list-inside space-y-1 text-sm text-gray-600 max-h-40 overflow-y-auto">
              <li v-for="(ingredient, idx) in recipe.ingredients" :key="idx">
                {{ ingredient }}
              </li>
            </ul>
          </div>

          <!-- Instructions -->
          <div class="mb-4">
            <h4 class="font-semibold text-gray-700 mb-2">Instructions:</h4>
            <ol class="list-decimal list-inside space-y-2 text-sm text-gray-600 max-h-40 overflow-y-auto">
              <li v-for="(instruction, idx) in recipe.instructions" :key="idx">
                {{ instruction }}
              </li>
            </ol>
          </div>

          <!-- Recipe Link -->
          <div class="mt-4 pt-4 border-t border-gray-200">
            <a 
              :href="recipe.url" 
              target="_blank" 
              rel="noopener noreferrer"
              class="text-blue-600 hover:text-blue-800 font-medium text-sm inline-flex items-center"
            >
              View Original Recipe
              <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
              </svg>
            </a>
          </div>

          <!-- Error Message if any -->
          <div v-if="recipe.error" class="mt-2 p-2 bg-yellow-100 border border-yellow-400 rounded text-sm text-yellow-700">
            <p class="font-semibold">Note:</p>
            <p>{{ recipe.error }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  recipes: {
    type: Array,
    required: true
  }
})

const handleImageError = (event) => {
  event.target.style.display = 'none'
}
</script>
