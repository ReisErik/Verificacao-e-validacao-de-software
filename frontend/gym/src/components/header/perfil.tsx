import {
    Avatar,
    AvatarFallback,
    AvatarImage
} from "@/components/ui/avatar"

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

import type { User } from "@/schemas/user"

export default function Perfil( {user} : {user: User | null} ) {
    return (
        <DropdownMenu>
            <DropdownMenuTrigger>
                <div className="flex gap-2 items-center">
                    <Avatar>
                        <AvatarImage src="" />
                        <AvatarFallback>P</AvatarFallback>
                    </Avatar>
                    <span>{user?.first_name || "Nome"}</span>
                </div>
            </DropdownMenuTrigger>

            <DropdownMenuContent>
                <DropdownMenuItem>
                    Perfil
                </DropdownMenuItem>
                <DropdownMenuItem>
                    Configurações
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}