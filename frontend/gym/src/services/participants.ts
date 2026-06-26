import { api } from "./api";

export async function getAllChallengeParticipate() {
    const response = await api.get(`/challenge/participant/get/all`);
    return response.data   
}

export async function leaveChallenge(challenge_id: number){
    const response = await api.delete(`/challenge/participant/leave/${challenge_id}`);
    return response.data
}