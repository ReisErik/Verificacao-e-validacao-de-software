import { useEffect, useState } from "react";

import InviteCard from "./inviteCard";

import type { Invite } from "@/schemas/invite";
import { getAllReceivedInvites } from "@/services/invite";

interface InvitePanelProps {
  compact?: boolean;
}

export default function InvitePanel({
  compact = false,
}: InvitePanelProps) {
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

  const pendingInvites = invites.filter(
    (invite) => invite.answer === null
  );

  const displayedInvites = compact
    ? pendingInvites.slice(0, 3)
    : pendingInvites;

  if (displayedInvites.length === 0) {
    return <h1>Nenhum convite pendente.</h1>;
  }

  return (
    <div className="space-y-4">
      {displayedInvites.map((invite) => (
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

