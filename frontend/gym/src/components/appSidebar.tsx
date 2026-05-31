import { Link } from "react-router-dom"

import {
  Home,
  Dumbbell,
  BarChart3,
  LogOut,
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
    title: "Página Inicial",
    path: "/",
    icon: Home,
  },
  {
    title: "Treinos",
    path: "/treinos",
    icon: Dumbbell,
  },
  {
    title: "Dashboard",
    path: "/dashboard",
    icon: BarChart3,
  },
]

export default function AppSidebar() {
  return (
    <Sidebar variant="inset">
      <SidebarHeader>
        <div className="px-2 py-4">
          <h1 className="text-lg font-bold">
            Gym Manager
          </h1>

          <p className="text-sm text-muted-foreground">
            Academia cadastrada
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
            <SidebarMenuButton>
              <LogOut />
              <span>Sair</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}