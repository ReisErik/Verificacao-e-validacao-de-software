import { z } from "zod"

export const loginSchema = z.object({
  email: z.email("Email inválido"),
  password: z
  .string()
  .min(6, "Senha deve ter pelo menos 6 caracteres"),
})

export type LoginSchema = z.infer<typeof loginSchema>