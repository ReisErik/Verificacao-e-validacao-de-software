import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

import type { Invite } from "@/schemas/invite";

interface InviteCardProps {
  invite: Invite;
  onAccept?: (inviteId: number) => void;
  onReject?: (inviteId: number) => void;
}

export default function InviteCard({
  invite,
  onAccept,
  onReject,
}: InviteCardProps) {
  return (
    <Card>
      <CardContent className="flex w-full items-center justify-between pl-4 pr-4">

        <div className="flex flex-col items-start">
            <p className="text-sm text-muted-foreground">{invite.sender_id} Convidou você para:</p>
            <h2 className="text-lg font-semibold">
            Desafio {invite.challenge_id}
            </h2>
        </div>

        <div className="flex gap-2">
          <Button onClick={() => onAccept?.(invite.id)}>Aceitar</Button>

          <Button variant="destructive" onClick={() => onReject?.(invite.id)}>
            Recusar
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
