import ChallengePanel from "@/components/challenges/challengePainel";
import InvitePanel from "@/components/invites/invitePanel";
import ReceivedInvites from "@/components/invites/receivedInvite";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function HomeUser() {
  return (
    <div className="ml-4">
      <Card className="p-4">
        <CardHeader>
          <CardTitle>Meus Desafios</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <ChallengePanel compact/>
        </CardContent>
      </Card>
      <Card className="p-4 mt-2">
        <CardHeader>
          <CardTitle>Convites</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <ReceivedInvites compact/>
        </CardContent>
      </Card>
    </div>
  );
}
