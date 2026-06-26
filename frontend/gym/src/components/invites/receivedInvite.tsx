import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";

import {
  getAllReceivedInvites,
  answerInvite,
} from "@/services/invite";

interface ReceivedInvitesProps {
  compact?: boolean;
}

export default function ReceivedInvites({
  compact = false
} : ReceivedInvitesProps) {
  const [invites, setInvites] = useState<any[]>([]);

  async function load() {
    try {
      setInvites(await getAllReceivedInvites());
    } catch {
      setInvites([]);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function respond(
    invite: any,
    answer: boolean
  ) {
    await answerInvite({
      invite_id: invite.id,
      challenge_id: invite.challenge_id,
      answer,
    });

    load();
  }

  const displayedInvites = compact ? 
    invites.filter(
      (invites) => invites.answer === null
    ).slice(0,3)
    :
    invites

  return (
    <div className="space-y-3">

      {displayedInvites.map((invite) => (
        <div
          key={invite.id}
          className="rounded-lg border p-4 flex justify-between items-center"
        >
          <div>

            <p className="font-semibold">
              {invite.challenge_name}
            </p>

            <p className="text-sm text-muted-foreground">
              {invite.sender_name}
            </p>

          </div>

          {invite.answer ? (
            <div>
              <p>Convite Respondido</p>
            </div>
            ) : (
              <div className="flex gap-2">
              <Button
                onClick={() =>
                  respond(invite, true)
                }
              >
                Aceitar
              </Button>

              <Button
                variant="destructive"
                onClick={() =>
                  respond(invite, false)
                }
              >
                Recusar
              </Button>
            </div>  
          )
          }
        </div>
      ))}

      {invites.length === 0 && (
        <p>Nenhum convite recebido.</p>
      )}

    </div>
  );
}