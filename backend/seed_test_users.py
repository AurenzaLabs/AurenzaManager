"""
Seed test users for local QA.

Run from repository root:
    python backend/seed_test_users.py

Or from backend folder:
    python seed_test_users.py
"""

try:
    from backend.database import users_col
    from backend.auth import hash_password
except ModuleNotFoundError:
    from database import users_col
    from auth import hash_password


TEST_USERS = [
    {
        "name": "Super Admin",
        "email": "superadmin@aurenza.test",
        "password": "SuperAdmin@123",
        "role": "SUPER_ADMIN",
    },
    {
        "name": "Admin User",
        "email": "admin@aurenza.test",
        "password": "Admin@123",
        "role": "ADMIN",
    },
    {
        "name": "Project Manager",
        "email": "pm@aurenza.test",
        "password": "Pm@12345",
        "role": "PM",
    },
    {
        "name": "Employee User",
        "email": "employee@aurenza.test",
        "password": "Employee@123",
        "role": "EMPLOYEE",
    },
]


def seed_users():
    for user in TEST_USERS:
        users_col.update_one(
            {"email": user["email"]},
            {
                "$set": {
                    "name": user["name"],
                    "email": user["email"],
                    "password": hash_password(user["password"]),
                    "role": user["role"],
                    "active": True,
                }
            },
            upsert=True,
        )


if __name__ == "__main__":
    seed_users()
    print("Seeded test users:")
    for user in TEST_USERS:
        print(f"- {user['role']}: {user['email']} / {user['password']}")
