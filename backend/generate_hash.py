from auth import hash_password as get_password_hash

print("admin ->", get_password_hash("admin"))
print("password ->", get_password_hash("password"))
