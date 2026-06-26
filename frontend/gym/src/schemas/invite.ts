import z from "zod";

export const InviteSchema = z.object({
  sender_id: z.number(),
  challenge_id: z.number(),
  answer: z.boolean() || null,
  id: z.number(),
  receiver_id: z.number(),
  sent: z.boolean(),
  sender_name: z.string()
});

export type Invite = z.infer<typeof InviteSchema>;

export const InviteAnswerSchema = z.object({
  invite_id: z.number(),
  challenge_id: z.number(),
  answer: z.boolean()
})

export type InviteAnswer = z.infer<typeof InviteAnswerSchema>;