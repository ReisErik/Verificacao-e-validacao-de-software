import { 
    Card, 
    CardContent, 
} from "@/components/ui/card"

import {
    Hand
} from "lucide-react"

import Perfil from "@/components/header/perfil"
import { useAuth } from "@/contexts/AuthContext"

export default function Header(){
    const workoutTodayReady = false
    const workout = "Treino A"
    const { user } = useAuth()
    return (
        <>
            <Card className="m-4">

                <CardContent className="flex justify-between items-center">
                    <div className="flex flex-col items-start">
                        <div className="flex gap-4 items-center">
                            <h2>Olá, {user?.first_name || "Teste"}!</h2>
                            <Hand></Hand>
                        </div>
                        <p>Pronto para enfrentar novos desafios hoje?</p>
                    </div>
                    <Perfil user={user} />
                </CardContent>
                
            </Card>
        </>
    )
}