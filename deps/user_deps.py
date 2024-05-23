from models.user_model import User
from services.user_service import UserService
from schemas.user_schema import Auth0User
from core.security import auth


async def get_current_user(auth_result: dict, token: str) -> User:
    email = auth_result["email"]
    user = await UserService.get_user_by_email(email)
    if not user:
        user_profile = await auth.get_user_profile(token)
        new_user = Auth0User(**user_profile)
        user = await UserService.create_user(new_user)
        return user
    return user
