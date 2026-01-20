from faker import Faker
from ms_fa.models import App, Permission, Role
from .base import Seeder


class AppSeeder(Seeder):
    priority = 30
    
    def run(self) -> None:
        faker = Faker()
        
        # Get permissions
        p_user_device_create = self.db.query(Permission).filter_by(
            name='User - Device - create'
        ).first()
        p_user_validate_email = self.db.query(Permission).filter_by(
            name='User - validate email'
        ).first()
        p_merchant_app_create = self.db.query(Permission).filter_by(
            name='Merchant - App - create'
        ).first()
        p_merchant_app_list = self.db.query(Permission).filter_by(
            name='Merchant - App - list'
        ).first()
        
        # Get roles
        r_merchant_app = self.db.query(Role).filter_by(name='merchant_app').first()
        
        apps = [
            {"app": App({"name": "aquarius", "description": "Aquarius"})},
            {"app": App({"name": "aquarius-front", "description": "Front de AQ"})},
            {"app": App({"name": "autobot", "description": None})},
            {
                "app": App({"name": "mobile_app", "description": None}),
                "permissions": [p for p in [p_user_device_create, p_user_validate_email] if p],
            },
            {"app": App({"name": "ms_financial_model_engine", "description": None})},
            {
                "app": App({"name": "ms_merchants", "description": None}),
                "permissions": [p for p in [p_merchant_app_create, p_merchant_app_list] if p],
                "roles": [r_merchant_app] if r_merchant_app else [],
            },
            {"app": App({"name": "ms_products", "description": None})},
            {
                "app": App({"name": "ms_single_signon", "description": None}),
                "permissions": [p_user_validate_email] if p_user_validate_email else [],
            },
        ]
        
        for item in apps:
            app_data = item["app"]
            existing = self.db.query(App).filter_by(name=app_data.name).first()
            
            if existing is None:
                self.db.add(app_data)
                self.db.flush()
                
                if "permissions" in item and item["permissions"]:
                    for p in item["permissions"]:
                        if p:
                            app_data.permissions.append(p)
                
                if "roles" in item and item["roles"]:
                    for r in item["roles"]:
                        if r:
                            app_data.roles.append(r)
                
                print(f"  ✓ Created app: {app_data.name}")
        
        self.commit()
