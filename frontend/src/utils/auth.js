import { jwtDecode } from 'jwt-decode';

export const getUserIdFromToken = () => {
  const token = localStorage.getItem('token');
  if (!token) return null;

  try {
    const decoded = jwtDecode(token);
    return decoded.user_id;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
}; 
