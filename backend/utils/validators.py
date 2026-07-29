import re

def sanitize_string(val):
    if not isinstance(val, str):
        return str(val)
    # Strip dangerous HTML/Script tags
    clean = re.sub(r'<[^>]*>', '', val)
    clean = clean.strip()
    return clean

def validate_predict_input(data):
    errors = []
    
    if not isinstance(data, dict):
        return False, ["Invalid payload format. Expected JSON object."]
        
    # Validate Age
    if "age" not in data:
        errors.append("Field 'age' is required.")
    else:
        try:
            age = int(data["age"])
            if age < 18 or age > 120:
                errors.append("Age must be an integer between 18 and 120.")
        except (ValueError, TypeError):
            errors.append("Age must be a valid number.")

    # Validate Sex
    if "sex" not in data:
        errors.append("Field 'sex' is required.")
    else:
        sex = sanitize_string(data["sex"]).lower()
        if sex not in ["male", "female"]:
            errors.append("Sex must be either 'male' or 'female'.")

    # Validate BMI
    if "bmi" not in data:
        errors.append("Field 'bmi' is required.")
    else:
        try:
            bmi = float(data["bmi"])
            if bmi < 10.0 or bmi > 70.0:
                errors.append("BMI must be a float between 10.0 and 70.0.")
        except (ValueError, TypeError):
            errors.append("BMI must be a valid number.")

    # Validate Children
    if "children" not in data:
        errors.append("Field 'children' is required.")
    else:
        try:
            children = int(data["children"])
            if children < 0 or children > 20:
                errors.append("Children must be an integer between 0 and 20.")
        except (ValueError, TypeError):
            errors.append("Children must be a valid number.")

    # Validate Smoker
    if "smoker" not in data:
        errors.append("Field 'smoker' is required.")
    else:
        smoker = sanitize_string(data["smoker"]).lower()
        if smoker not in ["yes", "no"]:
            errors.append("Smoker must be either 'yes' or 'no'.")

    # Validate Region
    if "region" not in data:
        errors.append("Field 'region' is required.")
    else:
        region = sanitize_string(data["region"]).lower()
        valid_regions = ["southwest", "southeast", "northwest", "northeast"]
        if region not in valid_regions:
            errors.append(f"Region must be one of {valid_regions}.")

    return len(errors) == 0, errors
