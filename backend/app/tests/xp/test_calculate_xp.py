from datetime import datetime, timedelta, UTC

from app.services.calculate_xp import calculate_xp
from app.schemas.challenge_schema import ChallengeType


BASE_DATE = datetime(2025, 1, 1, tzinfo=UTC)


def test_calculate_xp_streak_minimum():
    xp = calculate_xp(
        goal=3,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=3),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 100

def test_calculate_xp_streak_maximum():
    xp = calculate_xp(
        goal=30,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=30),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 360

def test_calculate_xp_streak_middle():
    xp = calculate_xp(
        goal=16.5,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=16),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 220


def test_calculate_xp_time_minimum():
    xp = calculate_xp(
        goal=1.75, 
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=7),
        challenge_type=ChallengeType.TIME,
    )

    assert xp == 105

def test_calculate_xp_time_maximum():
    xp = calculate_xp(
        goal=21, 
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=7),
        challenge_type=ChallengeType.TIME,
    )

    assert xp == 286

def test_calculate_xp_amount_minimum():
    xp = calculate_xp(
        goal=7,  
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=7),
        challenge_type=ChallengeType.AMOUNT,
    )

    assert xp == 105


def test_calculate_xp_amount_maximum():
    xp = calculate_xp(
        goal=140,  
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=7),
        challenge_type=ChallengeType.AMOUNT,
    )

    assert xp == 287

def test_calculate_xp_category_bonus_estudos():
    xp = calculate_xp(
        goal=3,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=3),
        challenge_type=ChallengeType.STREAK,
        category="Estudos",
    )

    assert xp == 120

def test_calculate_xp_category_bonus_exercicio():
    xp = calculate_xp(
        goal=3,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=3),
        challenge_type=ChallengeType.STREAK,
        category="Exercicio",
    )

    assert xp == 130

def test_calculate_xp_unknown_category():
    xp = calculate_xp(
        goal=3,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=3),
        challenge_type=ChallengeType.STREAK,
        category="CategoriaInexistente",
    )

    assert xp == 100

def test_calculate_xp_duration_multiplier_7_days():
    xp = calculate_xp(
        goal=3,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=7),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 105


def test_calculate_xp_duration_multiplier_14_days():
    xp = calculate_xp(
        goal=14,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=14),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 199


def test_calculate_xp_duration_multiplier_21_days():
    xp = calculate_xp(
        goal=21,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=21),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 268


def test_calculate_xp_duration_multiplier_30_days():
    xp = calculate_xp(
        goal=30,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=30),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 360

def test_calculate_xp_below_minimum_clamps():
    xp = calculate_xp(
        goal=0,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=3),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 100

def test_calculate_xp_above_maximum_clamps():
    xp = calculate_xp(
        goal=100,
        start_date=BASE_DATE,
        end_date=BASE_DATE + timedelta(days=30),
        challenge_type=ChallengeType.STREAK,
    )

    assert xp == 360