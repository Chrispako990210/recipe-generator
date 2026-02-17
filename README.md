# Recipe Generator

This repository contains custom recipe management web applications.

## Projects

### 🍽️ Meal Prep Selector

A full-stack web application for generating randomized meal plans based on protein selections.

**Location**: `/meal-prep-app`

**Features**:
- Select quantities for different protein types (Chicken, Beef, Pork, Fish, Vegetarian)
- Randomly generates meal plans from a recipe database
- Scrapes recipe details (ingredients, instructions, images) from cooking websites
- Responsive design with TailwindCSS
- Single Docker container deployment

**Tech Stack**:
- Frontend: Vue.js 3, Vite, TailwindCSS
- Backend: Python 3.11, FastAPI
- Scraping: recipe-scrapers library

**Quick Start**:
```bash
cd meal-prep-app
docker build -t meal-prep-selector .
docker run -p 8000:8000 meal-prep-selector
```

Then open `http://localhost:8000` in your browser.

See the [meal-prep-app/README.md](meal-prep-app/README.md) for detailed documentation.
