import { Link } from "react-router-dom"

import {
  Home,
  Dumbbell,
  BarChart3,
  LogOut,
  Mail
} from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarGroup,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar"

const menuItems = [
  {
    title: "Início",
    path: "/",
    icon: Home,
  },
  {
    title: "Meus Desafios",
    path: "/desafios",
    icon: Dumbbell,
  },
  {
    title: "Convites",
    path: "/convites",
    icon: Mail,
  },
]

export default function AppSidebar() {
  
  return (
    <Sidebar variant="inset">
      <SidebarHeader>
        <div className="flex flex-col px-2 py-4 items-start">
          <h1 className="font-bold">
            Desafios
          </h1>

          <p className="text-sm text-muted-foreground">
            Supere seus limites
          </p>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            {menuItems.map((item) => {
              const Icon = item.icon

              return (
                <SidebarMenuItem key={item.path}>
                  <SidebarMenuButton asChild>
                    <Link to={item.path}>
                      <Icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              )
            })}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={() => {
                localStorage.removeItem("token")
                window.location.href = "/login"
              }}>
              <LogOut />
              <span>Sair</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}