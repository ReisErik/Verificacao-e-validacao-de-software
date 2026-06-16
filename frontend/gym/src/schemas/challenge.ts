import z from "zod"

export const ChallengeSchema = z.object({
    id: z.number(),
    owner: z.number(),
    name: z.string(),
    description: z.string(),
    xp_reward: z.number(),
    start_date: z.date(),
    end_date: z.date(),
    goal: z.number(),
    visibility: z.boolean(),
    type_challenge: z.string(),
})

export type Challenge = z.infer<typeof ChallengeSchema>

export const CreateChallengeSchema = z.object({
    owner: z.number(),
    name: z.string(),
    description: z.string(),
    xp_reward: z.number(),
    start_date: z.date(),
    end_date: z.date(),
    goal: z.number(),
    visibility: z.boolean(),
    type_challenge: z.string(),
})

export type CreateChallenge = z.infer<typeof CreateChallengeSchema>