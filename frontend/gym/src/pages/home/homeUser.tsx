import ChallengePanel from "@/components/challenges/challengePainel"
import InvitePanel from "@/components/invites/invitePanel"

export default function HomeUser() {
 
    return (
        <div className="ml-4">
            <ChallengePanel></ChallengePanel>
            <div className="max-w-140 mr-auto pt-2">
                <InvitePanel></InvitePanel>
            </div>
        </div>
    )
}