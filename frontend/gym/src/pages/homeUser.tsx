import { Button } from "@/components/ui/button"

export default function HomeUser() {
    return (
        <div>
            <h1>Home do Usuário</h1>
            <Button variant="outline" onClick={() => {
                localStorage.removeItem("token")
                window.location.href = "/login"
            }}>
                Logout
            </Button>
        </div>
    )
}