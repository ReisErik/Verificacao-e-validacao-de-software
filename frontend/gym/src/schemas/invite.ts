import z from "zod";

export const InviteSchema = z.object({
  sender_id: z.number(),
  challenge_id: z.number(),
  answer: z.boolean() || null,
  id: z.number(),
  receiver_id: z.number(),
  sent: z.boolean(),
});

export type Invite = z.infer<typeof InviteSchema>;
