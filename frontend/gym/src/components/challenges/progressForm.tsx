import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { updateProgress } from "@/services/progression";

interface Props {
  challengeId: number;
}

export default function ProgressForm({
  challengeId,
}: Props) {
  const [score, setScore] = useState("");

  async function handleSubmit() {
    try {
      await updateProgress({
        challenge_id: challengeId,
        score: Number(score),
      });

      window.location.reload();
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="space-y-2">

      <h3 className="font-semibold">
        Registrar progresso
      </h3>

      <Input
        type="number"
        value={score}
        onChange={(e) => setScore(e.target.value)}
      />

      <Button onClick={handleSubmit}>
        Atualizar progresso
      </Button>

    </div>
  );
}