import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"

import { api }  from "@/services/api"
import { toast } from "sonner"
import axios from "axios"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

import {
    Field, FieldDescription, FieldGroup, FieldLabel, FieldSet, FieldError
} from "@/components/ui/field"

const loginSchema = z.object({
  email: z.email("Email inválido"),
  password: z
    .string()
    .min(6, "Senha deve ter pelo menos 8 caracteres"),
})

type LoginSchema = z.infer<typeof loginSchema>

export default function LoginPage() {
  const form = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  async function onSubmit(data: LoginSchema) {

    try {
      const response = await api.post("/auth/login", data)
        toast.success("Login bem-sucedido!")
        console.log(response.data)
        localStorage.setItem("token", response.data.access_token)
    }   
    catch (error) {
        if (axios.isAxiosError(error)) {

        toast.error(
        error.response?.data?.detail ||
        "Erro ao fazer login"
        )

    } else {

        toast.error("Erro inesperado")

    }
  }
}

  return (
    <div className="flex min-h-screen items-center justify-center">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle>Login</CardTitle>
        </CardHeader>

        <CardContent>
            <form onSubmit={form.handleSubmit(onSubmit)} className="w-full">
                <FieldSet >
                    <FieldGroup>
                        <Field>
                            <FieldLabel>Email</FieldLabel>
                            <Input 
                                placeholder="Digite seu email" 
                                type="email" 
                                {...form.register("email")} 
                            />
                            {form.formState.errors.email && (
                                <FieldError>
                                    {form.formState.errors.email.message}
                                </FieldError>
                            )}
                        </Field>
                        <Field>
                            <FieldLabel>Senha</FieldLabel>
                            <Input 
                                placeholder="Digite sua senha" 
                                type="password" 
                                {...form.register("password")} 
                            />

                            {form.formState.errors.password && (
                                <FieldError>
                                    {form.formState.errors.password.message}
                                </FieldError>
                            )}
                        </Field>

                        <Button type="submit" className="w-full mt-4">
                            Entrar
                        </Button>
                    </FieldGroup>
                </FieldSet>
            </form>
        </CardContent>
      </Card>
    </div>
  )
}