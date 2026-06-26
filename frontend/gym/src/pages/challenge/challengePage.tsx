import { useState } from "react";

import ChallengePanel from "@/components/challenges/challengePainel";
import CreateChallengeDialog from "@/components/challenges/createChallengeDialog";

import { Button } from "@/components/ui/button";

export default function ChallengePage() {
  const [reloadKey, setReloadKey] = useState(0);

  function handleCreated() {
    setReloadKey((prev) => prev + 1);
  }

  return (
    <div className="flex max-w-7xl flex-col gap-6 p-6">
      <div className="flex items-center">
        <div>
          <h1 className="text-3xl font-bold">Meus desafios</h1>
          <p className="text-muted-foreground">
            Gerencie seus desafios e acompanhe sua evolução.
          </p>
        </div>

        <CreateChallengeDialog onCreated={handleCreated}>
          <Button>Criar desafio</Button>
        </CreateChallengeDialog>
      </div>

      <ChallengePanel key={reloadKey} compact={false} />
    </div>
  );
}