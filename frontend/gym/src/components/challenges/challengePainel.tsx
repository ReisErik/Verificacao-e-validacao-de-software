import { useEffect, useState } from "react";

import type { Challenge } from "@/schemas/challenge";
import { getAllChallenge } from "@/services/challenge";

import ChallengeCard from "./challengeCard";

export default function ChallengePanel() {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadChallenges() {
      try {
        const data = await getAllChallenge();
        setChallenges(data);
      } catch (error) {
        console.error("Erro ao carregar desafios:", error);
      } finally {
        setIsLoading(false);
      }
    }

    loadChallenges();
  }, []);

  if (isLoading) {
    return <h1>Carregando desafios...</h1>;
  }

  if (challenges.length === 0) {
    return <h1>Nenhum desafio encontrado.</h1>;
  }

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      {challenges.map((challenge) => (
        <ChallengeCard key={challenge.id} challenge={challenge} />
      ))}
    </div>
  );
}
