import { api } from "./api";
import type { CreateChallenge } from "@/schemas/challenge"

export async function createChallenge(data : CreateChallenge){
    const response = await api.post(`/challenge/create`, data);
    return response.data;
}

export async function getAllChallenge(){
    const response = await api.get(`/challenge/all`);
    return response.data;
}

export async function getChallenge(challenge_id: number){
    const response = await api.get(`/challenge/${challenge_id}`);
    return response.data;
}