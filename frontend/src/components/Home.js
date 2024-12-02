import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Header from './Header';
import { getElementError } from '@testing-library/react';
// import healthy from '../healthy.jpg';
// import rice from '../rice.jpg';
// import autumnsoup from '../autumnsoup.jpg';
// import dessert from '../dessert.jpg';




const UNITS = ["slice", "dash", "bunch", "dozen", "ounce", "tsp", "Tbsp", "cup", "quart", "pound", "gal", "N/A"];
function Home() {
  const [recipes, setRecipes] = useState([]); // State to store fetched recipes
  // const [ingredients, setIngredients] = useState([])
  // const [selectedIngredient, setSelectedIngredient] = useState("");
  const [error, setError] = useState(null);   // State to store errors (optional)
  const [loading, setLoading] = useState(true); // State to manage loading
  const [addedIngredients, setAddedIngredients] = useState([]);
  const [useCase, setUseCase] = useState("  ")
  const token = sessionStorage.getItem("token")

  const handleIngredientChange = event => {
    const selected = event.target.options[event.target.selectedIndex];
    const value = selected.value
    const text = selected.text
    if (text !== "Select Ingredient")
      setAddedIngredients(prevIngredients => [...prevIngredients.filter(ing => ing.value !== value), { value: value, text: text },]);
  };

  const handleDelRecipe = async (id) => {
    console.log(`deleting recipe[${id}]`)
    // let token = sessionStorage.getItem("token")
    const params = { id: id }
    try {
      const response = await axios.delete("https://recipe.naurot.com/recipes/delete", {
        headers: {
          Authorization: `Bearer ${token}`
        },
        params: params
      })
      console.log(`Response from deleting recipe[${id}]: ${response.data}`)
       document.getElementById(`${id}`).innerHTML = ""
    } catch (err) {
      console.log(`Error deleting recipe[${id}]: ${err}`)
    }
  }

  const handleAISearch = async (id) => {
    console.log("In ai search. id: ", id)
    try {
      const response = await axios.get("https://recipe.naurot.com/recipes/ai", {
        params: { id: id }
      })
      console.log(`Success in ai search: ${response.data}`)
    } catch (err) {
      console.error(`Error in AI search: ${err}`)
    }
  }

  const handleIngredientCancel = () => {
    setAddedIngredients([]);
  };

  const handleIngredientSearch = async (event) => {
    event.preventDefault()
    // const token = sessionStorage.getItem("token")
    const prepend = "ing="
    const joiner = "&"
    const ing_list = addedIngredients.map(ing => prepend + `${ing.value}`).join(joiner)
    // console.log("ing keys: " + ing_list)
    setLoading(true);
    try {
      const recipesResponse = await axios.get(`https://recipe.naurot.com/recipes/view?${ing_list}`, {
        headers: { Authorization: `Bearer ${token}` },
        withCredentials: true,
      })
      setRecipes(recipesResponse.data.recipes);
    } catch (err) {
      setError('Failed to fetch recipe info');
      console.error('Error fetching recipe info:', err.response || err.message);
    }
    setAddedIngredients([])
    setLoading(false)
  }

  function handleIngredientRemove(id) {
    console.log(id)
    setAddedIngredients(addedIngredients.filter(ing => ing.value !== id))
  }

 window.handleAccept =  async function (id){
    try {
      const response = await axios.patch("https://recipe.naurot.com/admin/recipe/accept", null, {
        headers: {
          Authorization: `Bearer ${token}`
        }, params: { id: id }
      })
      setUseCase("Accepted")
      console.log(response)
    } catch (err) {
      console.log(`Error in accepting recipe[${id}], error: ${err}`)
    } finally{
      document.getElementById(`${id}`).innerHTML = ""
    }
  }
 window.handleReject =  async function (id){
    try {
      const response = await axios.delete("https://recipe.naurot.com/admin/recipe/reject", {
        headers: {
          Authorization: `Bearer ${token}`
        }, params: { id: id }
      })
      setUseCase("Rejected")
      console.log(response)
    } catch (err) {
      console.log(`Error in rejecting recipe[${id}], error: ${err}`)
    } finally{
      document.getElementById(`${id}`).innerHTML = ""
    }
  }


  const handleButtonClick = async (buttonName) => {
    const rejectIng = async id => {
      try {
        const response = await axios.delete("https://recipe.naurot.com/admin/ingredient/reject", {
          headers: {
            Authorization: `Bearer ${token}`
          }, params: { id: id }
        })
        setUseCase("Rejected")
        console.log(response)
      } catch (err) {
        console.log(`Error in rejecting ing[${id}], error: ${err}`)
      } finally{
        document.getElementById(`${id}`).innerHTML = ""
      }
    }
    const acceptIng = async id => {
      try {
        const response = await axios.patch("https://recipe.naurot.com/admin/ingredient/accept", null, {
          headers: {
            Authorization: `Bearer ${token}`
          }, params: { id: id }
        })
        setUseCase("Accepted")
        console.log(response)
      } catch (err) {
        console.log(`Error in accepting ing[${id}], error: ${err}`)
      } finally{
        document.getElementById(`${id}`).innerHTML = ""
      }
    }
    const container = document.getElementById("admin-container")
    // const token = sessionStorage.getItem("token")
    let response
    switch (buttonName) {
      case "ing":
        container.innerHTML = ""
        setUseCase("Ingredient Approval/Rejection")
        try {
          response = await axios.get("https://recipe.naurot.com/admin/list/ingredients", {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          const ingHtml = response.data.map(
            ing => `
              <div id=${ing[0]}>
                <p key=${ing[0]}>${ing[1]}</p>
                <button class="accept-btn" id="${ing[0]}">+</button>
                <button class="reject-btn" id="${ing[0]}">-</button>
              </div>
            `
          ).join(""); // Combine into a single HTML string

          container.innerHTML = ingHtml

          // Add event listeners for accept buttons
          document.querySelectorAll(".accept-btn").forEach(button => {
            button.addEventListener("click", (event) => {
              const id = event.target.getAttribute("id");
              console.log(`Accepted ingredient with ID: ${id}`);
              acceptIng(id);
            });
          });

          // Add event listeners for reject buttons
          document.querySelectorAll(".reject-btn").forEach(button => {
            button.addEventListener("click", (event) => {
              const id = event.target.getAttribute("id");
              console.log(`Rejected ingredient with ID: ${id}`);
              rejectIng(id);
            });
          });
        } catch (err) {
          if (!response || !response.data) {
            setUseCase("No Unapproved Ingredients");
          } else {
            const errorMessage = err.response?.data?.message || err.message || "An error occurred";

            console.error(`Error in admin ingredient:`, errorMessage); // Log full error for debugging
          }
        }
        break

      case "recipes":
        container.innerHTML = `<script> </script>`
        setUseCase("Recipe Approval/Rejection")
        try {
          response = await axios.get("https://recipe.naurot.com/admin/list/recipes", {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          const recipes = response.data
          recipes.forEach(recipe => {
            const [creator_id, name, recipe_id, instructions] = recipe;
            console.log(`Creator ID: ${creator_id}`);
            console.log(`Recipe ID: ${recipe_id}`);
            console.log(`Name: ${name}`);
            console.log(`Instructions: ${instructions}`);
            console.log('---------------------------');
          });
          let recipeHtml = ''
          recipes.forEach(recipe => {
            const [creator_id, name, recipe_id, instructions] = recipe;
            recipeHtml += `
              <br>
              <div id=${recipe_id}>
                                    <img
                        className="recipe-image"
                        src="https://recipe.naurot.com/recipes/${recipe_id}.png"
                        alt={recipe.name}
                      />
                <p>Creator ID: ${creator_id}</p>
                <p>Recipe ID: ${recipe_id}</p>
                <p>Name: ${name}</p>
                <p>Instructions: ${instructions}</p>
                <button onclick="handleReject(${recipe_id})">Reject</button>
                <button onclick="handleAccept(${recipe_id})">Accept</button>
                <br><br>
              </div>
            `;
          });
          container.innerHTML = recipeHtml
          // document.addEventListener("DOMContentLoaded", () => {

          //   setRecipes(response.data[0]);
          // });
        } catch (err) {
          if (!response)
            setUseCase("No Unapproved/Eligible Recipes")
          else {

            console.log(`Error in admin recipes: ${err}`)
          }
        }
        break;

      case "users":
        container.innerHTML = ""
        setUseCase("User Authorization Changes")
        try {
          response = await axios.get("https://recipe.naurot.com/admin/list/users", {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          const responseHtml = response.data.map(
            u => `
              <ul>
                <li style="list-style-type: none;" key="${u[0]}">
                  ${u[0]} ${u[1]} ${u[2]} ${u[3]}
                    <label for="status-${u[0]}">Select an Option: </label>
                    <select id="status-${u[0]}">
                      <option  ${u[3] === 2 ? "selected" : ""} value="${u[0]},2">2</option>
                      <option  ${u[3] === 1 ? "selected" : ""} value="${u[0]},1">1</option>
                      <option  ${u[3] === 0 ? "selected" : ""} value="${u[0]},0">0</option>
                      <option value="${u[0]},ban">ban</option>
                    </select>
                </li>
              </ul>
            `
          ).join(""); // .join() ensures you get a single string from the map
          container.innerHTML = responseHtml
          container.addEventListener("change", async event => {
            const [id, lvl] = event.target.value.split(",")
            try {
              if (lvl === "ban") {
                // API call to remove user
                await axios.patch(`https://recipe.naurot.com/admin/remove_user`, null, {
                  headers: {
                    Authorization: `Bearer ${token}`
                  },
                  params: { id: id }
                });
                console.log(`User [${id}] has been banned.`);
              } else {
                // API call to change auth level
                await axios.patch(`https://recipe.naurot.com/admin/change_auth`, null, {
                  headers: {
                    Authorization: `Bearer ${token}`
                  },
                  params: { id: id, lvl: lvl }
                });
                console.log(`Auth level of user[${id}] has been changed to: ${lvl}.`);
              }
            } catch (err) {
              console.error(
                `Error processing request. User[${id}], Level: ${lvl}.`,
                err
              );
            }
          })
        } catch (err) {
          console.log(`Error in admin user changes: ${err}`)

        }

        // dropdown.addEventListener
        break;
      default:
        console.error("Error: reached default case")
        break
    }
  }

  useEffect(() => {
    const auth = sessionStorage.getItem("auth")
    // const token = sessionStorage.getItem("token");

    const fetchUserInfo = async () => {
      setLoading(true);
      try {
        const recipesResponse = await axios.get('https://recipe.naurot.com/recipes/view', {
          headers: { Authorization: `Bearer ${token}` },
          withCredentials: true,
        })
        setRecipes(recipesResponse.data.recipes);
        // console.log("recipes: " + JSON.stringify(recipesResponse.data.recipes));
      } catch (err) {
        setError('Failed to fetch recipe info');
        console.error('Error fetching recipe info:', err.response || err.message);
      }
      try {
        const ingredientsResponse = await axios.get("https://recipe.naurot.com/recipes/ingredients", {
          headers: { Authorization: `Bearer ${token}` },
          withCredentials: true,
        })
        localStorage.setItem("ingredients", JSON.stringify(ingredientsResponse.data))
      } catch (err) {
        setError('Failed to fetch ingredient info');
        console.error('Error fetching ingredient info:', err.response || err.message);
      } finally {
        setLoading(false);
      }
    };

    if (auth < 2)
      fetchUserInfo();
  }, [token]);

  return (
    <div>
      <Header onButtonClick={handleButtonClick} />
      <main>
        <h1>I Have No Mouth and I Must Eat</h1>
        {/* <p>Here you can explore various recipes!</p> */}
        {sessionStorage.getItem("auth") < 2 && <section className="goodeats">

          {loading && <p>Loading recipes...</p>} {/* Show a loading message */}
          {error && <p>{error}</p>} {/* Show an error message if fetching fails */}
          {!loading && !error && (
            <div className="container">

              <div className="scrollable-container">
                {recipes.map((recipe) => (
                  <div className="recipe-container" key={recipe.id} id={recipe.id}>
                    <div className="recipe-name">{recipe.name}</div>
                    <div className="recipe-content">
                      <img
                        className="recipe-image"
                        src={"https://recipe.naurot.com" + recipe.image}
                        alt={recipe.name}
                      />
                      <div className="recipe-ingredients">
                        {/* <span id="in-line"><h3>Ingredients</h3>{recipe.creator == user.id && <button >del</button>}</span> */}
                        <span id="in-line">
                          <h3>Ingredients</h3>
                          {/* <button onClick={() => handleAISearch(recipe.id)}>ai</button> */}
                          {recipe.creator == sessionStorage.getItem("id") && <button id={recipe.id} onClick={() => handleDelRecipe(recipe.id)}>del</button>}
                          </span>
                        <ul>
                          {recipe.ingredients.map((ingredient) => (
                            <li key={ingredient.ingredient_id}>
                              {ingredient.quantity} {UNITS[ingredient.unit]} of {ingredient.ingredient_name}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    <div className="recipe-instructions">
                      <h3>Instructions</h3>
                      <p>{recipe.instructions}</p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="right-container">
                <form id="ingredientForm" onSubmit={handleIngredientSearch}>
                  <div className="form-group">
                    <label>
                      <select id="ingredientSelect" onChange={handleIngredientChange} >

                        <option key="0">Select Ingredient</option>
                        {Object.entries(JSON.parse(localStorage.getItem("ingredients"))).map(([key, value]) => (
                          <option value={value} key={value}>
                            {key}
                          </option>
                        ))}
                      </select></label>
                  </div>

                  <br></br>
                  <div id="ingredients">
                    <ul id="add-ingredient-here">
                      {addedIngredients.map(ingredient =>
                        <li  key={ingredient.value}>{ingredient.text}<button onClick={() => handleIngredientRemove(ingredient.value)}>del</button></li>
                      )}
                    </ul>
                  </div>
                  <div className="button-box">
                    <button type="button" onClick={handleIngredientCancel}>Cancel</button><button>Submit</button>
                  </div>
                </form>
              </div>
            </div>
          )}
          {/* <div className="clearfix"></div> */}
        </section>}
        {sessionStorage.getItem("auth") > 1 && <section className="admin">
          <>
            <p>{useCase}</p>
            <div className="container">
              <div id="admin-container" className="scrollable-container">

              </div>
            </div>
          </>
        </section>}
      </main>
    </div>
  );
}

export default Home;
