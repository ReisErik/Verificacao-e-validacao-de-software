import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useEffect, useState } from "react";

import type { Challenge } from "@/schemas/challenge";
import type { Progression } from "@/schemas/progress";
import { getProgress } from "@/services/progression";

export default function ChallengeCard({challenge,}: {challenge: Challenge | null;}) {
    if (!challenge) return null;

    const [progression, setProgression] = useState<Progression | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const remainingDays = Math.max(0,Math.ceil((new Date(challenge.end_date).getTime() - Date.now()) / (1000 * 60 * 60 * 24)));

    useEffect(() => {
        let mounted = true;
        const challenge_id = challenge.id
        async function loadProgression() {
            try {
                const data = await getProgress(challenge_id);
                if (mounted) {
                    setProgression(data);
                }
            } catch (error) {
                console.error("Erro ao carregar progresso:", error);
            } finally {
                if (mounted) {
                    setIsLoading(false);
                }
            }
        }
        loadProgression();
        return () => {
            mounted = false;
        };
    } , [challenge.id]);

    if (isLoading) {
        return <h1>Loading...</h1>;
    }

    const progressValue = progression? (progression.current_progress / challenge.goal) * 100: 0;
    


    return (
        <Card>
            <CardContent className="space-y-2">
                <h1 className="text-lg font-bold">{challenge.name}</h1>
                <h2>{challenge.type_challenge}</h2>
                <p>{challenge.category}</p>

                <div>
                    <div className="flex justify-between mb-2">
                        <span>Progresso</span>
                        <span>
                            {progression?.current_progress ?? 0} / {challenge.goal}
                        </span>
                    </div>

                    <Progress value={progressValue} />

                    <div className="mt-2 text-sm">
                        Dias restantes: {remainingDays}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}