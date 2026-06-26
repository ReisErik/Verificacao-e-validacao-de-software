import axios from "axios";
import { api } from "./api";
import type { InviteAnswer } from "@/schemas/invite";

export async function getAllReceivedInvites() {
    try {
        const response = await api.get("/challenge/invite/received");
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.detail || "Erro ao buscar convites recebidos.");
        }
        throw error;
    }
}

export async function getAllSentInvites() {
    try {
        const response = await api.get("/challenge/invite/sent");
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.detail || "Erro ao buscar convites enviados.");
        }
        throw error;
    }
}

export async function sendInvite(
    challenge_id: number,
    user_invitated_id: number
) {
    try {
        const response = await api.post(
            `/challenge/invite/send/${challenge_id}/${user_invitated_id}`
        );
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.detail || "Erro ao enviar convite.");
        }
        throw error;
    }
}

export async function answerInvite(data: InviteAnswer) {
    try {
        const response = await api.post("/challenge/participant/join", data);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.detail || "Erro ao responder convite.");
        }
        throw error;
    }
}