import {z} from "zod"

export const UserSchema = z.object({
    id: z.number(),
    first_name: z.string(),
    last_name: z.string(),
    unique_name: z.string(),
    email: z.string(),
    role: z.enum(["admin", "user"]),
    active: z.boolean(),
})

export type User = z.infer<typeof UserSchema>