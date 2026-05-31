import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

import AppSidebar from "@/components/appSidebar"
import { Outlet } from "react-router-dom"

export default function Layout() {
  return (
      <SidebarProvider>
        <SidebarTrigger />
        <AppSidebar />

        <SidebarInset>
            <Outlet />
        </SidebarInset>

      </SidebarProvider>
  )
}