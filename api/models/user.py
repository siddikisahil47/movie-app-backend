from typing import Dict, Optional
from . import BaseModel
from passlib.hash import bcrypt
import re

class User(BaseModel):
    """User model for database operations."""
    table_name = "users"
    
    @classmethod
    async def find_by_email(cls, email: str) -> Optional[Dict]:
        """Find a user by email."""
        try:
            response = cls.get_db().table(cls.table_name).select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error finding user by email: {str(e)}")
    
    @classmethod
    async def create_user(cls, data: Dict) -> Dict:
        """Create a new user with password hashing."""
        validated_data = cls.validate_user_data(data)
        validated_data['password'] = bcrypt.hash(validated_data['password'])
        return await cls.create(validated_data)
    
    @classmethod
    def validate_user_data(cls, data: Dict) -> Dict:
        """Validate user data before creation/update."""
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            raise ValueError("Invalid email format")
        
        # Validate password strength
        if len(data['password']) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        return data
    
    @classmethod
    async def verify_password(cls, email: str, password: str) -> Optional[Dict]:
        """Verify user password and return user if valid."""
        user = await cls.find_by_email(email)
        if user and bcrypt.verify(password, user['password']):
            return user
        return None
