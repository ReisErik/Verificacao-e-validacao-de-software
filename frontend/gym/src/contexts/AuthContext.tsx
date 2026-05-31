import {
    createContext,
    useContext,
    useState,
    useEffect,
} from "react"

import { api } from "@/services/api"

type User = {
    id: number
    first_name: string
    last_name: string
    unique_name: string
    email: string
}

type AuthContextType = {
    user: User | null
    loading: boolean
    login: (email: string, password: string) => Promise<void>
    logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function LoadUser(){
            const token = localStorage.getItem("token")
            if(!token) {
                setLoading(false)
                return
            }

            try {
                const response = await api.get("/auth/me")
                setUser(response.data)
            }
            catch (error){
                localStorage.removeItem("token")
            }
            finally {
                setLoading(false)
            }
        }

        LoadUser()
    }, [])

    async function login(email: string, password: string) {
        const response = await api.post("/auth/login", {
            email,
            password
        })

        localStorage.setItem("token", response.data.access_token)
        setUser(response.data.user)
    }

    function logout() {
        localStorage.removeItem("token")
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)

    if(!context){
        throw new Error("useAuth precisa ser utilizado dentro de um AuthProvider")
    }

    return context
}