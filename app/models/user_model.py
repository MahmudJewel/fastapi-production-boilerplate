from sqlalchemy import Column, String, Enum
from enum import Enum as PythonEnum
from app.core.database import Base

from .common import CommonModel
from app.utils.constant.globals import UserRole

# class UserRole(str, PythonEnum):
# 	user = "user"
# 	admin = "admin"

class User(CommonModel):
	__tablename__ = "users"

	email = Column(String(50), unique=True, index=True)
	password = Column(String(50), nullable=True) # nullable=True for social auth(OAuth2)
	first_name = Column(String(50), nullable=True)
	last_name = Column(String(50), nullable=True)
	role = Column(Enum(UserRole), default=UserRole.USER)

	def __repr__(self):
		return f"{self.email}"
	
metadata = Base.metadata

