"""
Entry point for running CLI commands.

Usage:
    python -m ms_fa seed
    python -m ms_fa seed --fresh
    python -m ms_fa seed --seeder PermissionSeeder
    python -m ms_fa create-tables
    python -m ms_fa drop-tables
    python -m ms_fa createsuperuser
"""
from ms_fa.commands import main

if __name__ == "__main__":
    main()
