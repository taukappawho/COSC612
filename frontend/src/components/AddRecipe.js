import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function AddRecipe() {
  const [title, setTitle] = useState('');
  const [image, setImage] = useState(null);
  const [instructions, setInstructions] = useState('');
  const [ingredients, setIngredients] = useState([{
    name: '',
    quantity: '',
    unit: ''
  }]);
  const [approvedIngredients, setApprovedIngredients] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();


  useEffect(() => {
    const fetchIngredients = async () => {
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
        console.error('Failed to fetch ingredients:', error);
      }
    };
    fetchIngredients();
  }, []);

  const addIngredient = () => {
    setIngredients([...ingredients, { name: '', quantity: '', unit: '' }]);
  };

  const removeIngredient = (index) => {
    const newIngredients = ingredients.filter((_, i) => i !== index);
    setIngredients(newIngredients);
  };

  const handleIngredientChange = (index, field, value) => {
    const newIngredients = [...ingredients];
    newIngredients[index][field] = value;
    setIngredients(newIngredients);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title || !image || !instructions || ingredients.length === 0) {
      setMessage('Please fill in all required fields');
      return;
    }

    if (image.size > 5 * 1024 * 1024) {
      setMessage('Image size must be less than 5MB');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('image', image);
      formData.append('instructions', instructions);
      formData.append('ingredients', JSON.stringify(ingredients));

      await axios.post('http://localhost:8000/recipes/create',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );

      setMessage('Recipe submitted successfully! Awaiting admin approval.');
      setTimeout(() => navigate('/'), 2000);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Failed to submit recipe');
    }
  };

  return (
    <div className="container">
      <h1>Add New Recipe</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Recipe Title"
          maxLength="45"
          required
        />

        <input
          type="file"
          accept="image/png"
          onChange={(e) => setImage(e.target.files[0])}
          required
        />

        {ingredients.map((ing, index) => (
          <div key={index} className="form-group">
            <select
              value={ing.name}
              onChange={(e) => handleIngredientChange(index, 'name', e.target.value)}
              required
            >
              <option value="">Select Ingredient</option>
              {approvedIngredients.map(ingredient => (
                <option key={ingredient.id} value={ingredient.name}>
                  {ingredient.name}
                </option>
              ))}
              <option value="other">Other</option>
            </select>

            {ing.name === 'other' && (
              <input
                type="text"
                value={ing.customName}
                onChange={(e) => handleIngredientChange(index, 'customName', e.target.value)}
                placeholder="Enter ingredient name"
                maxLength="45"
                required
              />
            )}

            <input
              type="number"
              value={ing.quantity}
              onChange={(e) => handleIngredientChange(index, 'quantity', e.target.value)}
              placeholder="Quantity"
              min="0"
              step="any"
              required
            />

            <select
              value={ing.unit}
              onChange={(e) => handleIngredientChange(index, 'unit', e.target.value)}
              required
            >
              <option value="">Unit</option>
              <option value="oz">oz</option>
              <option value="lb">lb</option>
              <option value="grams">grams</option>
              <option value="mL">mL</option>
              <option value="cup">cup</option>
              <option value="tsp">teaspoon</option>
              <option value="tbsp">tablespoon</option>
            </select>

            <button type="button" onClick={() => removeIngredient(index)}>X</button>
          </div>
        ))}

        <button type="button" onClick={() => navigate('/')}>Cancel</button>
        <button type="button" onClick={addIngredient}>Add Ingredient</button>

        <textarea
          value={instructions}
          onChange={(e) => setInstructions(e.target.value)}
          placeholder="Cooking Instructions"
          required
        />

        <div className="button-group">
          <button type="submit" className="buttonform">Submit Recipe</button>
          <button type="button" onClick={() => navigate('/')}>Cancel</button>
        </div>
      </form>

      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default AddRecipe;
