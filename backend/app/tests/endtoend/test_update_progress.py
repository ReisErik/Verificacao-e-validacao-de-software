from playwright.sync_api import expect
from datetime import date, timedelta

def test_invite_challenge_e2e(logged_page):

    page = logged_page

    page.goto("http://localhost:5173/desafios")

    page.get_by_test_id(
        "open-create-challenge"
    ).click()

    expect(
        page.get_by_role(
            "heading",
            name="Criar desafio"
        )
    ).to_be_visible()

    page.get_by_label("Nome").fill("Desafio Playwright")

    page.get_by_label("Descrição").fill(
        "Criado automaticamente"
    )

    page.get_by_label("Meta").fill("10")

    page.get_by_label(
        "Número máximo de participantes"
    ).fill("5")

    today = date.today()

    page.get_by_label("Data inicial").fill(today.strftime("%Y-%m-%d"))

    page.get_by_label("Data final").fill((today + timedelta(days=10)).strftime("%Y-%m-%d"))

    page.get_by_test_id(
        "create-challenge"
    ).click()

    page.get_by_text("Desafio Playwright").click()

    page.get_by_text("Atualizar Progresso").click()

    page.wait_for_load_state("networkidle")

    page.get_by_text("Desafio Playwright").click()

    expect(
        page.get_by_text("1 / 10")
    ).to_be_visible()

    page.get_by_test_id(
        "delete-challenge"
    ).click()

    page.get_by_test_id(
        "confirm-delete"
    ).click()

    expect(
        page.locator("text=Desafio Playwright")
    ).to_have_count(0)
