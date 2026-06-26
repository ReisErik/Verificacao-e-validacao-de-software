import { useEffect, useState } from "react";

import type { Challenge } from "@/schemas/challenge";
import { getAllChallengeParticipate } from "@/services/participants";

import ChallengeCard from "./challengeCard";

interface ChallengePanelProps {
  compact?: boolean;
}

export default function ChallengePanel({compact = false} : ChallengePanelProps) {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  async function loadChallenges() {
    try {
      const data = await getAllChallengeParticipate();
      setChallenges(data);
    } catch (error) {
      console.error("Erro ao carregar desafios:", error);
    } finally {
      setIsLoading(false);
    }
  }
  
  useEffect(() => {
    loadChallenges();
  }, []);

  if (isLoading) {
    return <h1>Carregando desafios...</h1>;
  }

  if (challenges.length === 0) {
    return <h1>Nenhum desafio encontrado.</h1>;
  }

  const displayedChallenges = compact 
  ? challenges.slice(0,3) : challenges

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      {displayedChallenges.map((challenge) => (
        <ChallengeCard key={challenge.id} challenge={challenge} onLeave={loadChallenges} />
      ))}
    </div>
  );
}
