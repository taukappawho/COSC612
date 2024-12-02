import React from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function CreateRecipe() {
    //   const [username, setUsername] = useState('');
    //   const [email, setEmail] = useState('');
    //   const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const token = sessionStorage.getItem('token');
    if (!token) {
        console.error('No token found in sessionStorage');
        return;
    }

    const handleOnClick = async () => {
        try {
            const response = await axios.get('https://recipe.naurot.com/recipes/create',

                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': `Bearer ${token}`,
                    }
                }
            );
            console.log('Response:', response.data);

        } catch (error) {
            console.error('Error object:', error);
            console.error('Error response:', error.response);
        }
    };

    return (
        <button onClick={handleOnClick}>Create Recipe</button>
    );
}

export default CreateRecipe;
