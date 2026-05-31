import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "@/contexts/AuthContext"

import { toast } from "sonner"
import axios from "axios"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

import {
    Field, FieldGroup, FieldLabel, FieldSet, FieldError
} from "@/components/ui/field"

import { type LoginSchema, loginSchema } from "@/pages/login/loginSchema"

export default function LoginPage() {

    const navigate = useNavigate()
    const [loading, setLoading] = useState(false)
    const { login } = useAuth()

    const form = useForm<LoginSchema>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            email: "",
            password: "",
        },
    })
    
    async function onSubmit(data: LoginSchema) {
        
        setLoading(true)
        
        try {
            await login(data.email, data.password)
            toast.success("Login bem-sucedido!")
            navigate("/")
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
        finally {
            setLoading(false)
        }
    }
    
    return (
        <div className="flex min-h-screen items-center justify-center">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Login</CardTitle>
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

                        <Button type="submit" 
                                className="w-full mt-4"
                                disabled={loading}
                        >
                            {loading ? "Entrando..." : "Entrar"}
                        </Button>
                    </FieldGroup>
                </FieldSet>
            </form>
        </CardContent>
      </Card>
    </div>
  )
}