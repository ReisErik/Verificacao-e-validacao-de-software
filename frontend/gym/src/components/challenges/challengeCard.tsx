import {
    Card,
    CardContent
} from "@/components/ui/card"

import type { Challenge } from "@/schemas/challenge"

export default function ChallengeCard( {challenge} : { challenge : Challenge | null} ){
    return(
        <>
        <Card>
            <CardContent>
                <h1>{challenge?.name || "Nome do desafio"}</h1>
            </CardContent>
        </Card>
        </>
    )
}