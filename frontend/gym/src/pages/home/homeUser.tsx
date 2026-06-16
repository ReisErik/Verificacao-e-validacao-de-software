import ChallengeCard from "@/components/challenges/challengeCard"

export default function HomeUser() {
    const challenge_mock = {
        name:"teste"
    }
    
    return (
        <div>
            <h1>Home do Usuário</h1>
            <ChallengeCard challenge={challenge_mock}></ChallengeCard>
        </div>
    )
}