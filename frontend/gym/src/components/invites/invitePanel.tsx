import { useEffect, useState } from "react";

import InviteCard from "./inviteCard";

import type { Invite } from "@/schemas/invite";
import { getAllReceivedInvites } from "@/services/invite";

export default function InvitePanel() {
  const [invites, setInvites] = useState<Invite[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadInvites() {
      try {
        const data = await getAllReceivedInvites();
        setInvites(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    loadInvites();
  }, []);

  if (loading) {
    return <h1>Carregando convites...</h1>;
  }

  if (invites.length === 0) {
    return <h1>Nenhum convite recebido.</h1>;
  }

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      {invites.map((invite) => (
        <InviteCard
          key={invite.id}
          invite={invite}
          onAccept={(id) => console.log("Aceitou", id)}
          onReject={(id) => console.log("Recusou", id)}
        />
      ))}
    </div>
  );
}