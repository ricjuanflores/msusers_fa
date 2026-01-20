from random import randint
from faker import Faker
from ms_fa.models import Role, User
from .base import Seeder


class UserSeeder(Seeder):
    priority = 20
    
    def run(self) -> None:
        faker = Faker()
        
        # Get roles
        admin_role = self.db.query(Role).filter_by(name="root").first()
        shopper_role = self.db.query(Role).filter_by(name="shopper").first()
        merchant_root_role = self.db.query(Role).filter_by(name="merchant_root").first()
        merchant_admin_role = self.db.query(Role).filter_by(name="merchant_admin").first()
        merchant_role = self.db.query(Role).filter_by(name="merchant").first()
        
        users = [
            {
                "id": "accd5294-aab2-4b61-96b5-fd7f39ee6de1",
                "name": "root",
                "email": "root@example.com",
                "phone": "0000000000",
                "role": admin_role,
            },
            {
                "id": "231df84e-608f-4d11-82aa-7ee32f14882c",
                "name": "merchant_root",
                "email": "merchant_root@example.com",
                "phone": "0000000001",
                "role": merchant_root_role
            },
            {
                "id": "1c5680b7-7361-4159-8634-5791e15c03ff",
                "name": "merchant_admin",
                "email": "merchant_admin@example.com",
                "phone": "0000000002",
                "role": merchant_admin_role
            },
            {
                "id": "7bc84a8c-aef6-4186-8875-34b287e8321d",
                "name": "merchant_single",
                "email": "merchant_single@example.com",
                "phone": "0000000003",
                "role": merchant_role,
            },
            {
                "id": "4bd7a357-0670-4aa9-a261-6234b774f7fe",
                "name": "shopper",
                "email": "shopper@example.com",
                "phone": "9999999999",
                "role": shopper_role,
            }
        ]
        
        for user_data in users:
            existing = self.db.query(User).filter_by(email=user_data.get("email")).first()
            
            if not existing:
                user = User({
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "phone": user_data.get("phone"),
                })
                user.id = user_data.get("id")
                user.is_active = True
                user.set_password('secret')
                
                if user_data.get("role"):
                    user.roles.append(user_data.get("role"))
                
                self.db.add(user)
                print(f"  ✓ Created user: {user_data.get('email')}")
        
        # Create random shoppers
        for i in range(5):
            email = faker.unique.email()
            existing = self.db.query(User).filter_by(email=email).first()
            
            if not existing and shopper_role:
                shopper = User({
                    "phone": faker.unique.msisdn()[:15],
                    "email": email,
                    "name": faker.first_name(),
                    "lastname": faker.last_name(),
                    "second_lastname": faker.last_name(),
                })
                shopper.is_active = bool(randint(0, 1))
                shopper.set_password("secret")
                shopper.roles.append(shopper_role)
                self.db.add(shopper)
                print(f"  ✓ Created random shopper: {email}")
        
        self.commit()
