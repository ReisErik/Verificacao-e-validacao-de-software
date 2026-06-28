from playwright.sync_api import Page, expect

def test_login(page: Page):

    page.goto("http://localhost:5173/login")

    page.get_by_placeholder("Digite seu email").fill("user@user.com")

    page.get_by_placeholder("Digite sua senha").fill("user")

    page.get_by_role("button", name="Entrar").click()

    expect(page).to_have_url("http://localhost:5173/")