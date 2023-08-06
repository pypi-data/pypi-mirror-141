def register_user_validate(attrs):
    if "username" in attrs and len(attrs.get("username")) >= 10:
        return "username should not more than 10 characters"
    elif "phone_number" in attrs and len(attrs.get("phone_number")) >= 14:
        return "Please valid phone number"
    elif "password" in attrs and len(attrs.get("password")) < 6:
        return "Password should be more than 6 characters"
    else:
        pass
