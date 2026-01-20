from faker import Faker
from ms_fa.models import Role, Permission
from .base import Seeder


class RoleSeeder(Seeder):
    priority = 20
    
    def run(self) -> None:
        faker = Faker()
        
        # Get permissions
        p_user_shopper_update_profile = self.db.query(Permission).filter_by(
            name='User - Shopper - update profile'
        ).first()
        
        p_admin = self.db.query(Permission).all()
        
        p_merchant_admin = self.db.query(Permission).filter(
            Permission.name.in_([
                "Merchant - Admin - create",
                "Merchant - Admin - list",
                "Merchant - Admin - update",
                "Merchant - Admin - delete",
            ])
        ).all()
        
        p_merchant_app = self.db.query(Permission).filter_by(
            name='Merchant - App - list'
        ).first()
        
        p_merchant = self.db.query(Permission).filter(
            Permission.name.in_([
                "Merchant - Admin - create",
                "Merchant - Admin - list",
                "Merchant - Admin - update",
                "Merchant - Admin - delete",
            ])
        ).all()
        
        p_acquisition_admin = self.db.query(Permission).filter(
            Permission.name.in_([
                'Product - ProductBranch - validate',
                'Product - ProductBranch - delete',
            ])
        ).all()
        
        roles = [
            {"role": Role({"name": "root", "fixed": True})},
            {"role": Role({"name": "admin", "fixed": True}), "permissions": p_admin},
            {"role": Role({"name": "application", "fixed": True})},
            {
                "role": Role({"name": "shopper", "fixed": True}),
                "permissions": [p_user_shopper_update_profile] if p_user_shopper_update_profile else []
            },
            {"role": Role({"name": "user", "fixed": True})},
            {"role": Role({"name": "merchant_root", "fixed": True})},
            {"role": Role({"name": "merchant_admin", "fixed": True}), "permissions": p_merchant_admin},
            {
                "role": Role({"name": "merchant_app", "fixed": True}),
                "permissions": [p_merchant_app] if p_merchant_app else []
            },
            {"role": Role({"name": "merchant", "fixed": True}), "permissions": p_merchant},
            {"role": Role({"name": "financial", "fixed": True})},
            {"role": Role({"name": "financial_user", "fixed": True})},
            {"role": Role({"name": "lambda_user", "fixed": True})},
            {"role": Role({"name": "quash_user", "fixed": True})},
            {"role": Role({"name": "cashier_user", "fixed": True})},
            {"role": Role({"name": "acquisition", "fixed": True})},
            {"role": Role({"name": "acquisition_admin", "fixed": True}), "permissions": p_acquisition_admin},
        ]
        
        for item in roles:
            role_data = item["role"]
            existing = self.db.query(Role).filter_by(name=role_data.name).first()
            
            if existing is None:
                self.db.add(role_data)
                self.db.flush()  # Get the ID
                
                if "permissions" in item and item["permissions"]:
                    for p in item["permissions"]:
                        if p:
                            role_data.permissions.append(p)
                
                print(f"  ✓ Created role: {role_data.name}")
        
        self.commit()
