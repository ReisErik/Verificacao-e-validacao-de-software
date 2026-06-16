import { api } from "./api";

export async function getAllReceivedInvites(){
    const response = await api.get(`/challenge/invite/received`);
    return response.data;
}

