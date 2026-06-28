import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { getAllChallengeParticipate } from "@/services/participants";
import { getAllUsers } from "@/services/users";
import { sendInvite } from "@/services/invite";

export default function CreateInviteForm() {
  const [challengeId, setChallengeId] = useState("");
  const [userId, setUserId] = useState("");

  const [challenges, setChallenges] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const c = await getAllChallengeParticipate();
        setChallenges(c);
      } catch {}

      try {
        const u = await getAllUsers();
        setUsers(u);
      } catch {}
    }

    load();
  }, []);

  async function handleCreate() {
    if (!challengeId || !userId) return;

    await sendInvite(Number(challengeId), Number(userId));

    setChallengeId("");
    setUserId("");
  }

  return (
    <div className="max-w-lg space-y-4">

      <div>
        <Label>Desafio</Label>

        <Select
          value={challengeId}
          onValueChange={setChallengeId}
        >
          <SelectTrigger>
            <SelectValue placeholder="Selecione um desafio" />
          </SelectTrigger>

          <SelectContent>
            {challenges.map((challenge) => (
              <SelectItem
                key={challenge.id}
                value={String(challenge.id)}
              >
                {challenge.name ??
                  `Desafio ${challenge.name}`}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

      </div>

      <div>
        <Label>Usuário</Label>

        <Select
          value={userId}
          onValueChange={setUserId}
        >
          <SelectTrigger>
            <SelectValue placeholder="Selecione um usuário" />
          </SelectTrigger>

          <SelectContent>
            {users.map((user) => (
              <SelectItem
                key={user.id}
                value={String(user.id)}
              >
                {user.first_name} (@{user.unique_name})
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

      </div>

      <Button
        className="w-full"
        onClick={handleCreate}
        data-testid="invite"
      >
        Enviar convite
      </Button>

    </div>
  );
}