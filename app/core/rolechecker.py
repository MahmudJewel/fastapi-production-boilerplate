from fastapi import FastAPI, Depends, HTTPException
from app.schemas.user_schema import User
from app.api.endpoints.user import user_function as UserFunctions


# Role based access control
class RoleChecker:
	def __init__(self, allowed_roles: list[str]):
		self.allowed_roles = allowed_roles

	# import auth
	def __call__(self, user: User = Depends(UserFunctions.get_current_user)):
		if user.role not in self.allowed_roles:
			# logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
			raise HTTPException(status_code=403, detail="You are not allowed to access the API")

