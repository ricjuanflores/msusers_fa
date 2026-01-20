from .base import Seeder
from .permission_seeder import PermissionSeeder
from .role_seeder import RoleSeeder
from .user_seeder import UserSeeder
from .app_seeder import AppSeeder

# Lista de seeders en orden de ejecución (por prioridad)
SEEDERS = [
    PermissionSeeder,  # priority: 10
    RoleSeeder,        # priority: 20
    UserSeeder,        # priority: 20
    AppSeeder,         # priority: 30
]

__all__ = [
    "Seeder",
    "PermissionSeeder",
    "RoleSeeder",
    "UserSeeder",
    "AppSeeder",
    "SEEDERS",
]
