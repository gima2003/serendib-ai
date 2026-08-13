import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import datetime

class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    country_code: str = Field(..., min_length=2, max_length=3)
    preferred_currency: str = Field(..., min_length=3, max_length=3)
    password: str = Field(..., min_length=8)
    confirm_password: str

    @field_validator('email')
    @classmethod
    def email_lowercase(cls, v):
        return v.lower()

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegister':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        
        # password strength validation
        if not re.search(r'[A-Z]', self.password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', self.password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', self.password):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
            raise ValueError('Password must contain at least one special character')
            
        return self

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    country_code: str
    preferred_currency: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
