import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";

import CreateInviteForm from "@/components/invites/createInviteForm";
import ReceivedInvites from "@/components/invites/receivedInvite";
import SentInvites from "@/components/invites/sentInvite";

export default function InvitePage() {
  return (
    <div className="max-w-7xl p-6 space-y-6">

      <div>

        <h1 className="text-3xl font-bold">
          Convites
        </h1>

        <p className="text-muted-foreground">
          Gerencie convites enviados e recebidos.
        </p>

      </div>

      <Tabs defaultValue="received">

        <TabsList>

          <TabsTrigger value="create">
            Criar
          </TabsTrigger>

          <TabsTrigger value="received">
            Recebidos
          </TabsTrigger>

          <TabsTrigger value="sent">
            Enviados
          </TabsTrigger>

        </TabsList>

        <TabsContent value="create">
          <CreateInviteForm />
        </TabsContent>

        <TabsContent value="received">
          <ReceivedInvites />
        </TabsContent>

        <TabsContent value="sent">
          <SentInvites />
        </TabsContent>

      </Tabs>

    </div>
  );
}