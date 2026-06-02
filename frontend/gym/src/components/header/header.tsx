import { 
    Card, 
    CardContent, 
} from "@/components/ui/card"

import { 
    Flame, 
    Rocket, 
    Dumbbell,
    Clock,
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
                    <div className="flex items-center gap-3">
                        <span className=" text-2xl font-bold">
                            0
                        </span>

                        <div className="flex flex-col items-center">
                            <Flame className="text-red-500"/>
                            <span className="text-sm text-red-500">Streak</span>
                        </div> 
                    </div>

                    <div className="flex items-center gap-2">
                        {workoutTodayReady ? (
                            <>
                                <Rocket/>
                                <span>Tá pago!</span>
                            </>
                        ) : (
                            <>
                                <Dumbbell/>
                                <div className="flex flex-col items-start">
                                <span>Hoje é dia de</span>
                                    <span className="font-bold">{workout}</span>
                                </div>
                            </>
                        )}
                    </div>

                    <div className="flex gap-2 items-center">
                        <Clock/>
                        <div className="flex flex-col items-start">
                            <span className="text-sm text-muted-foreground">Treino as 18:00</span>
                            {workoutTodayReady ? (
                                <span className="text-sm text-green-500">Treino Realizado</span>
                            ) : (
                                <span className="text-sm text-red-500">Pendente</span>
                            )}
                        </div>
                    </div>
                    
                    <Perfil user={user} />
                </CardContent>
                
            </Card>
        </>
    )
}