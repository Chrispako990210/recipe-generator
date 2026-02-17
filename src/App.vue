<template>
  <div class="app">
    <h1>Meal Prep Selector</h1>
    <div class="form">
      <h2>Select Ingredients</h2>
      <div class="ingredient-input">
        <label>
          Chicken:
          <input type="number" v-model.number="ingredients.chicken" min="0" />
        </label>
      </div>
      <div class="ingredient-input">
        <label>
          Beef:
          <input type="number" v-model.number="ingredients.beef" min="0" />
        </label>
      </div>
      <div class="ingredient-input">
        <label>
          Pasta:
          <input type="number" v-model.number="ingredients.pasta" min="0" />
        </label>
      </div>
      <div class="ingredient-input">
        <label>
          Vegetarian:
          <input type="number" v-model.number="ingredients.vegetarian" min="0" />
        </label>
      </div>
      <button @click="generateRecipes" :disabled="loading">
        {{ loading ? 'Generating...' : 'Generate Recipes' }}
      </button>
    </div>
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div v-if="recipes.length > 0" class="recipes">
      <h2>Generated Recipes</h2>
      <div v-for="(recipe, index) in recipes" :key="index" class="recipe-card">
        <h3>{{ recipe.title }}</h3>
        <p v-if="recipe.host"><strong>Source:</strong> {{ recipe.host }}</p>
        <p v-if="recipe.total_time"><strong>Total Time:</strong> {{ recipe.total_time }} minutes</p>
        <p v-if="recipe.yields"><strong>Yields:</strong> {{ recipe.yields }}</p>
        <div v-if="recipe.ingredients && recipe.ingredients.length > 0">
          <h4>Ingredients:</h4>
          <ul>
            <li v-for="(ingredient, idx) in recipe.ingredients" :key="idx">{{ ingredient }}</li>
          </ul>
        </div>
        <div v-if="recipe.instructions_list && recipe.instructions_list.length > 0">
          <h4>Instructions:</h4>
          <ol>
            <li v-for="(instruction, idx) in recipe.instructions_list" :key="idx">{{ instruction }}</li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      ingredients: {
        chicken: 2,
        beef: 0,
        pasta: 1,
        vegetarian: 0
      },
      recipes: [],
      loading: false,
      error: null
    }
  },
  methods: {
    async generateRecipes() {
      this.loading = true
      this.error = null
      this.recipes = []
      
      try {
        const response = await fetch('/api/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.ingredients)
        })
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        this.recipes = data.recipes || []
      } catch (err) {
        this.error = `Failed to generate recipes: ${err.message}`
        console.error(err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #2c3e50;
  text-align: center;
}

.form {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.ingredient-input {
  margin: 10px 0;
}

.ingredient-input label {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ingredient-input input {
  padding: 5px;
  width: 80px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

button:hover:not(:disabled) {
  background: #35a372;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.recipes {
  margin-top: 20px;
}

.recipe-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.recipe-card h3 {
  color: #2c3e50;
  margin-top: 0;
}

.recipe-card h4 {
  color: #42b983;
  margin-top: 15px;
}

.recipe-card ul, .recipe-card ol {
  margin: 10px 0;
  padding-left: 25px;
}

.recipe-card li {
  margin: 5px 0;
}
</style>
