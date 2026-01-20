from faker import Faker
from ms_fa.models import Permission
from .base import Seeder


class PermissionSeeder(Seeder):
    priority = 10
    
    def run(self) -> None:
        faker = Faker()
        
        permissions = [
            # User permissions
            Permission({"name": "User - Role - list", "fixed": True}),
            Permission({"name": "User - Role - detail", "fixed": True}),
            Permission({"name": "User - Permission - list", "fixed": True}),
            Permission({"name": "User - Permission - detail", "fixed": True}),
            Permission({"name": "User - create", "fixed": True}),
            Permission({"name": "User - list", "fixed": True}),
            Permission({"name": "User - detail", "fixed": True}),
            Permission({"name": "User - update", "fixed": True}),
            Permission({"name": "User - update password", "fixed": True}),
            Permission({"name": "User - update available credit", "fixed": True}),
            Permission({"name": "User - update total debt", "fixed": True}),
            Permission({"name": "User - list devices", "fixed": True}),
            Permission({"name": "User - permissions", "fixed": True}),
            Permission({"name": "User - roles", "fixed": True}),
            Permission({"name": "User - activate", "fixed": True}),
            Permission({"name": "User - soft delete", "fixed": True}),
            Permission({"name": "User - restore", "fixed": True}),
            Permission({"name": "User - delete", "fixed": True}),
            Permission({"name": "User - validate email", "fixed": True}),
            Permission({"name": "User - generate token", "fixed": True}),
            
            # App permissions
            Permission({"name": "User - App - create", "fixed": True}),
            Permission({"name": "User - App - list", "fixed": True}),
            Permission({"name": "User - App - detail", "fixed": True}),
            Permission({"name": "User - App - generate token", "fixed": True}),
            Permission({"name": "User - App - update", "fixed": True}),
            Permission({"name": "User - App - permissions", "fixed": True}),
            Permission({"name": "User - App - roles", "fixed": True}),
            Permission({"name": "User - App - delete", "fixed": True}),
            
            # Device permissions
            Permission({"name": "User - Device - list", "fixed": True}),
            Permission({"name": "User - Device - create", "fixed": True}),
            Permission({"name": "User - Device - detail", "fixed": True}),
            Permission({"name": "User - Device - update", "fixed": True}),
            Permission({"name": "User - Device - delete", "fixed": True}),
            
            # Shopper permissions
            Permission({"name": "User - Shopper - create", "fixed": True}),
            Permission({"name": "User - Shopper - list", "fixed": True}),
            Permission({"name": "User - Shopper - detail", "fixed": True}),
            Permission({"name": "User - Shopper - update", "fixed": True}),
            Permission({"name": "User - Shopper - upload files", "fixed": True}),
            Permission({"name": "User - Shopper - update profile", "fixed": True}),
            Permission({"name": "User - Shopper - update kyc prescoring", "fixed": True}),
            Permission({"name": "User - Shopper - update second credit", "fixed": True}),
            Permission({"name": "User - Shopper - update payment", "fixed": True}),
            
            # Feature Flags
            Permission({"name": "Feature Flags - service - create", "fixed": True}),
            Permission({"name": "Feature Flags - service - list", "fixed": True}),
            Permission({"name": "Feature Flags - service - detail", "fixed": True}),
            Permission({"name": "Feature Flags - service - update", "fixed": True}),
            Permission({"name": "Feature Flags - service - delete", "fixed": True}),
            Permission({"name": "Feature Flags - feature - create", "fixed": True}),
            Permission({"name": "Feature Flags - feature - list", "fixed": True}),
            Permission({"name": "Feature Flags - feature - detail", "fixed": True}),
            Permission({"name": "Feature Flags - feature - update", "fixed": True}),
            Permission({"name": "Feature Flags - feature - update status", "fixed": True}),
            Permission({"name": "Feature Flags - feature - delete", "fixed": True}),
            
            # Analytics
            Permission({"name": "Analytics - event - create", "fixed": True}),
            Permission({"name": "Analytics - counters - list", "fixed": True}),
            
            # Merchants
            Permission({"name": "Merchant - Admin - create", "fixed": True}),
            Permission({"name": "Merchant - Admin - list", "fixed": True}),
            Permission({"name": "Merchant - Admin - update", "fixed": True}),
            Permission({"name": "Merchant - Admin - delete", "fixed": True}),
            Permission({"name": "Merchant - Client - create", "fixed": True}),
            Permission({"name": "Merchant - Client - list", "fixed": True}),
            Permission({"name": "Merchant - Client - update", "fixed": True}),
            Permission({"name": "Merchant - Client - delete", "fixed": True}),
            Permission({"name": "Merchant - App - create", "fixed": True}),
            Permission({"name": "Merchant - App - list", "fixed": True}),
            Permission({"name": "Merchant - App - update", "fixed": True}),
            Permission({"name": "Merchant - App - delete", "fixed": True}),
            
            # Products
            Permission({"name": "Product - Brand - create", "fixed": True}),
            Permission({"name": "Product - Brand - get", "fixed": True}),
            Permission({"name": "Product - Brand - list", "fixed": True}),
            Permission({"name": "Product - Brand - update", "fixed": True}),
            Permission({"name": "Product - Brand - delete", "fixed": True}),
            Permission({"name": "Product - Category - create", "fixed": True}),
            Permission({"name": "Product - Category - get", "fixed": True}),
            Permission({"name": "Product - Category - list", "fixed": True}),
            Permission({"name": "Product - Category - update", "fixed": True}),
            Permission({"name": "Product - Category - delete", "fixed": True}),
            Permission({"name": "Product - Product - create", "fixed": True}),
            Permission({"name": "Product - Product - get", "fixed": True}),
            Permission({"name": "Product - Product - list", "fixed": True}),
            Permission({"name": "Product - Product - update", "fixed": True}),
            Permission({"name": "Product - Product - delete", "fixed": True}),
            Permission({"name": "Product - ProductBranch - create", "fixed": True}),
            Permission({"name": "Product - ProductBranch - get", "fixed": True}),
            Permission({"name": "Product - ProductBranch - list", "fixed": True}),
            Permission({"name": "Product - ProductBranch - update", "fixed": True}),
            Permission({"name": "Product - ProductBranch - delete", "fixed": True}),
            Permission({"name": "Product - ProductBranch - validate", "fixed": True}),
            Permission({"name": "Product - Promo - create", "fixed": True}),
            Permission({"name": "Product - Promo - get", "fixed": True}),
            Permission({"name": "Product - Promo - list", "fixed": True}),
            Permission({"name": "Product - Promo - update", "fixed": True}),
            Permission({"name": "Product - Promo - delete", "fixed": True}),
        ]
        
        for perm in permissions:
            existing = self.db.query(Permission).filter_by(name=perm.name).first()
            if existing is None:
                self.db.add(perm)
                print(f"  ✓ Created permission: {perm.name}")
        
        self.commit()
