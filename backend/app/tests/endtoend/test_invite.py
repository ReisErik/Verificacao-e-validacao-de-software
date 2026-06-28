from playwright.sync_api import expect

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

    page.get_by_label("Data inicial").fill("2026-12-01")

    page.get_by_label("Data final").fill("2026-12-15")

    page.get_by_test_id(
        "create-challenge"
    ).click()

    expect(
        page.locator("text=Desafio Playwright")
    ).to_have_count(1)

    page.goto("http://localhost:5173/convites")

    page.get_by_test_id("criar").click()

    page.get_by_text("Selecione um desafio").click()
    page.get_by_text("Desafio Playwright").click()

    page.get_by_text("Selecione um usuário").click()
    page.get_by_text("user2").click()

    page.get_by_test_id("invite").click()
    page.keyboard.press("Escape")

    page.get_by_test_id("enviados").click()

    expect(
        page.locator("text=Desafio Playwright")
    ).to_have_count(1)

    page.goto("http://localhost:5173/desafios")

    page.get_by_text("Desafio Playwright").click()

    page.get_by_test_id(
        "delete-challenge"
    ).click()

    page.get_by_test_id(
        "confirm-delete"
    ).click()

    page.wait_for_load_state("networkidle")
    
    expect(
        page.locator("text=Desafio Playwright")
    ).to_have_count(0)
