from datetime import datetime
from app.schemas.challenge_schema import ChallengeType
from app.utils.calculate_duration_days import calculate_duration_days

def calculate_xp(
    goal: float,
    start_date: datetime,
    end_date: datetime,
    challenge_type: ChallengeType,
    category: str | None = None,
) -> int:

    duration_days = calculate_duration_days(start_date, end_date)

    base_xp = 50

    if challenge_type == ChallengeType.STREAK:
        normalized_effort = (goal - 3) / (30 - 3)

    elif challenge_type == ChallengeType.TIME:
        hours_per_day = goal / duration_days
        normalized_effort = (hours_per_day - 0.25) / (3 - 0.25)

    else: 
        amount_per_day = goal / duration_days
        normalized_effort = (amount_per_day - 1) / (20 - 1)

    normalized_effort = max(0.0, min(normalized_effort, 1.0))

    effort_xp = 50 + normalized_effort * 200

    category_bonus = {
        "Leitura": 10,
        "Exercicio": 30,
        "Estudos": 20,
        "Idiomas": 15,
        "Saude": 30,
    }.get(category or "", 0)

    subtotal = base_xp + effort_xp + category_bonus

    if duration_days >= 30:
        multiplier = 1.20
    elif duration_days >= 21:
        multiplier = 1.15
    elif duration_days >= 14:
        multiplier = 1.10
    elif duration_days >= 7:
        multiplier = 1.05
    else:
        multiplier = 1.00

    final_xp = int(subtotal * multiplier)

    return final_xp