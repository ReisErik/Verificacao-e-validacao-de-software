import { useEffect, useState } from "react";

import { getAllSentInvites } from "@/services/invite";

export default function SentInvites() {
  const [invites, setInvites] = useState<any[]>([]);

  useEffect(() => {
    async function load() {
      try {
        setInvites(await getAllSentInvites());
      } catch {
        setInvites([]);
      }
    }

    load();
  }, []);

  return (
    <div className="space-y-3">

      {invites.map((invite) => (
        <div
          key={invite.id}
          className="rounded-lg border p-4"
        >
          <p className="font-semibold">
            {invite.challenge_name}
          </p>

          <p className="text-sm text-muted-foreground">
            Para: {invite.receiver_name ??
              invite.receiver_id}
          </p>

          <p className="text-sm text-muted-foreground">
            Status:{" "}
            {invite.answer === null
              ? "Pendente"
              : invite.answer
              ? "Aceito"
              : "Recusado"}
          </p>
        </div>
      ))}

      {invites.length === 0 && (
        <p>Nenhum convite enviado.</p>
      )}

    </div>
  );
}