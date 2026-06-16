import { z } from "zod"

export const loginSchema = z.object({
  email: z.email("Email inválido"),
  password: z
  .string()
  .min(4, "Senha deve ter pelo menos 4 caracteres"),
})

export type LoginSchema = z.infer<typeof loginSchema>