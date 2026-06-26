import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useEffect, useState } from "react";

import type { Challenge } from "@/schemas/challenge";
import type { Progression } from "@/schemas/progress";
import { getProgress } from "@/services/progression";
import ProgressForm from "./progressForm";

import { Button } from "@/components/ui/button";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTrigger,
  AlertDialogTitle,
  AlertDialogCancel,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogAction
} from "@/components/ui/alert-dialog";

import { leaveChallenge } from "@/services/participants";

export default function ChallengeCard({
  challenge,
  onLeave,
}: {
  challenge: Challenge | null;
  onLeave: (challenge_id: number) => void;
}) {
  if (!challenge) return null;

  const [progression, setProgression] = useState<Progression | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const remainingDays = Math.max(
    0,
    Math.ceil(
      (new Date(challenge.end_date).getTime() - Date.now()) /
        (1000 * 60 * 60 * 24),
    ),
  );

  useEffect(() => {
    let mounted = true;
    const challenge_id = challenge.id;
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
  }, [challenge.id]);

  const handleConfirmLeave = async () => {
    try {
      await leaveChallenge(challenge.id);
      onLeave(challenge.id);
    } catch (error) {
      console.error(error);
    }
  };

  if (isLoading) {
    return <h1>Loading...</h1>;
  }

  const progressValue = progression
    ? (progression.current_progress / challenge.goal) * 100
    : 0;
  const percent = ((progression?.current_progress ?? 0) / challenge.goal) * 100;

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Card>
          <CardContent className="space-y-2">
            <h1 className="text-lg font-bold">{challenge.name}</h1>
            <h2>{challenge.type_challenge}</h2>
            <p>{challenge.category}</p>

            <Progress value={progressValue} />

            <div className="text-sm">Dias restantes: {remainingDays}</div>
          </CardContent>
        </Card>
      </DialogTrigger>

      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{challenge.name}</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <p>{challenge.description}</p>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <strong>Categoria</strong>
              <p>{challenge.category}</p>
            </div>

            <div>
              <strong>Tipo</strong>
              <p>{challenge.type_challenge}</p>
            </div>

            <div>
              <strong>Modo</strong>
              <p>{challenge.mode_challenge}</p>
            </div>

            <div>
              <strong>XP</strong>
              <p>{challenge.xp_reward}</p>
            </div>

            <div>
              <strong>Meta</strong>
              <p>{challenge.goal}</p>
            </div>

            <div>
              <strong>Progresso</strong>
              <p>
                {progression?.current_progress ?? 0} / {challenge.goal}
              </p>
            </div>
          </div>

          <Progress value={percent} />

          <ProgressForm challengeId={challenge.id} />
        </div>

        <AlertDialog>

          <AlertDialogTrigger>
            <Button variant="destructive">Sair do desafio</Button>
          </AlertDialogTrigger>

          <AlertDialogContent>
        
            <AlertDialogHeader>
              <AlertDialogTitle>Tem certeza?</AlertDialogTitle>
              <AlertDialogDescription>
                Você vai deixar de participar desse desafio e essa ação pode ser
                irreversível
              </AlertDialogDescription>
            </AlertDialogHeader>

            <AlertDialogFooter>
              <AlertDialogCancel>Cancelar</AlertDialogCancel>
              <AlertDialogAction variant="destructive" onClick={handleConfirmLeave}>
                Confirmar
              </AlertDialogAction>
            </AlertDialogFooter>

          </AlertDialogContent>

        </AlertDialog>

      </DialogContent>
    </Dialog>
  );
}
