import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Header from './Header';
import { getUserIdFromToken } from '../utils/auth';

function Home() {
  const [recipes, setRecipes] = useState([]);
  const [offset, setOffset] = useState(0);
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [approvedIngredients, setApprovedIngredients] = useState([]);
  const limit = 30;

  const fetchRecipes = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found');
        return;
      }

      const params = new URLSearchParams({
        offset: offset,
        limit: limit,
        ingredients: selectedIngredients.join(',')
      });

      const response = await axios.get(
        `http://localhost:8000/recipes?${params}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      setRecipes(response.data);
    } catch (error) {
      console.error('Failed to fetch recipes:', error);
    }
  }, [offset, selectedIngredients, limit]);

  const fetchApprovedIngredients = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found');
        return;
      }

      const response = await axios.get('http://localhost:8000/ingredients', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setApprovedIngredients(response.data);
    } catch (error) {
      console.error('Error fetching ingredients:', error);
    }
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      await fetchRecipes();
      await fetchApprovedIngredients();
    };
    fetchData();
  }, [offset, selectedIngredients, fetchRecipes, fetchApprovedIngredients]);

  const handleDelete = async (recipeId) => {
    try {
      await axios.delete(`http://localhost:8000/recipes/${recipeId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      fetchRecipes();
    } catch (error) {
      console.error('Failed to delete recipe:', error);
    }
  };

  const handleAISearch = async (recipeId) => {
    try {
      const response = await axios.get(`http://localhost:8000/recipes/similar/${recipeId}`);
      setRecipes(response.data);
    } catch (error) {
      console.error('Failed to find similar recipes:', error);
    }
  };

  return (
    <div>
      <Header />
      <main>
        <h1>I Have No Mouth and I Must Eat</h1>
        <p>Here you can explore various recipes!</p>
        <section className="goodeats">
          <div className="filter-section">
            <select
              onChange={(e) => {
                if (e.target.value) {
                  setSelectedIngredients(prev => [...prev, e.target.value]);
                }
              }}
            >
              <option value="">Filter by Ingredient</option>
              {approvedIngredients.map(ing => (
                <option key={ing.id} value={ing.id}>{ing.name}</option>
              ))}
            </select>
            {selectedIngredients.length > 0 && (
              <button onClick={() => setSelectedIngredients([])}>Clear Filters</button>
            )}
          </div>

          <div className="recipe-grid">
            {recipes.map(recipe => (
              <div key={recipe.id} className="responsive">
                <div className="gallery">
                  <img src={`/images/image_${recipe.id}.png`} alt={recipe.title} />
                  <div className="desc">
                    <h3>{recipe.title}</h3>
                    <p>{recipe.instructions}</p>
                    <div className="recipe-actions">
                      {recipe.userId === getUserIdFromToken() && (
                        <button onClick={() => handleDelete(recipe.id)}>Delete</button>
                      )}
                      <button onClick={() => handleAISearch(recipe.id)}>Find Similar</button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="clearfix"></div>

          {recipes.length === limit && (
            <button onClick={() => setOffset(prev => prev + limit)}>Load More</button>
          )}
        </section>
      </main>
    </div>
  );
}

export default Home;
