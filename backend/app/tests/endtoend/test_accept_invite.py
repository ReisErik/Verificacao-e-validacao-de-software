from playwright.sync_api import expect

def test_invite_challenge_e2e(browser):

    ctx1 = browser.new_context()
    page1 = ctx1.new_page()

    page1.goto("http://localhost:5173/login")
    page1.get_by_placeholder("Digite seu email").fill("user@user.com")
    page1.get_by_placeholder("Digite sua senha").fill("user")
    page1.get_by_role("button", name="Entrar").click()
    page1.wait_for_url("**/")

    ctx2 = browser.new_context()
    page2 = ctx2.new_page()

    page2.goto("http://localhost:5173/login")
    page2.get_by_placeholder("Digite seu email").fill("user2@user2.com")
    page2.get_by_placeholder("Digite sua senha").fill("user2")
    page2.get_by_role("button", name="Entrar").click()
    page2.wait_for_url("**/")

    page1.goto("http://localhost:5173/desafios")

    page1.get_by_test_id("open-create-challenge").click()

    page1.get_by_label("Nome").fill("Desafio Playwright")
    page1.get_by_label("Descrição").fill("Criado automaticamente")
    page1.get_by_label("Meta").fill("10")
    page1.get_by_label("Número máximo de participantes").fill("5")
    page1.get_by_label("Data inicial").fill("2026-12-01")
    page1.get_by_label("Data final").fill("2026-12-15")

    page1.get_by_test_id("create-challenge").click()

    expect(page1.get_by_text("Desafio Playwright")).to_be_visible()

    page1.goto("http://localhost:5173/convites")

    page1.get_by_test_id("criar").click()
    page1.get_by_text("Selecione um desafio").click()
    page1.get_by_text("Desafio Playwright").click()

    page1.get_by_text("Selecione um usuário").click()
    page1.get_by_text("user2").click()

    page1.get_by_test_id("invite").click()

    page2.goto("http://localhost:5173/convites")

    page2.get_by_text("Aceitar").click()

    expect(page2.get_by_text("Desafio Playwright")).to_be_visible()

    page1.goto("http://localhost:5173/desafios")
    page2.goto("http://localhost:5173/desafios")

    page2.get_by_text("Desafio Playwright").click()

    page2.get_by_test_id(
        "delete-challenge"
    ).click()

    page2.get_by_test_id(
        "confirm-delete"
    ).click()

    page1.get_by_text("Desafio Playwright").click()

    page1.get_by_test_id(
        "delete-challenge"
    ).click()

    page1.get_by_test_id(
        "confirm-delete"
    ).click()

    page1.close()
    page2.close()
    ctx1.close()
    ctx2.close()