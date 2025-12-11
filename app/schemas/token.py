from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    user_id: str
    username: str


class RefreshTokenRequest(BaseModel):
    """Request schema for refreshing tokens"""
    refresh_token: str
