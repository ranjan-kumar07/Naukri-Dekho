from .models import Profile


def calculate_profile_completion(profile):

    score = 0
    total = 10  # we will divide into 10 parts

    # 1. Profile Image
    if profile.profile_image:
        score += 1

    # 2. Phone
    if profile.phone:
        score += 1

    # 3. Location
    if profile.location:
        score += 1

    # 4. Bio
    if profile.bio:
        score += 1

    # 5. Resume
    if profile.resume:
        score += 1

    # 6. Skills
    if profile.skills.exists():
        score += 1

    # 7. Education
    if profile.educations.exists():
        score += 1

    # 8. Experience
    if profile.experiences.exists():
        score += 1

    # 9. Projects
    if profile.projects.exists():
        score += 1

    # 10. Certifications
    if profile.certifications.exists():
        score += 1

    percentage = int((score / total) * 100)

    return percentage