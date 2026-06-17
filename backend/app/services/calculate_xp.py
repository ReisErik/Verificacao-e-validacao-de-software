from datetime import datetime
from app.schemas.challenge_schema import ChallengeType

def calculate_xp(
    goal: float,
    start_date: datetime,
    end_date: datetime,
    challenge_type: ChallengeType,
    category: str | None = None,
) -> int:

    duration_days = max((end_date - start_date).days, 1)

    base_xp = 50

    effort_per_day = goal / duration_days

    if challenge_type == ChallengeType.STREAK:
        normalized_effort = effort_per_day

    elif challenge_type == ChallengeType.TIME:
        normalized_effort = effort_per_day / 3

    else:
        normalized_effort = effort_per_day / 20

    effort_score = normalized_effort * 100

    if duration_days < 7:
        duration_bonus = duration_days * 2
    elif duration_days < 21:
        duration_bonus = duration_days * 3
    elif duration_days < 30:
        duration_bonus = duration_days * 4
    else:
        duration_bonus = duration_days * 5

    category_bonus = {
        "Leitura": 10,
        "Exercicio": 30,
        "Estudos": 20,
        "Idiomas": 15,
        "Saude": 30,
    }.get(category or "", 0)

    final_xp = int(
        base_xp
        + effort_score
        + duration_bonus
        + category_bonus
    )

    return max(50, min(final_xp, 1000))