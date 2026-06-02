import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

import AppSidebar from "@/components/sidebar/appSidebar"
import { Outlet } from "react-router-dom"
import Header from "@/components/header/header"

export default function Layout() {
  return (
      <SidebarProvider>
        <AppSidebar />
        <SidebarTrigger />

        <SidebarInset>
            <Header />
            <Outlet />
        </SidebarInset>

      </SidebarProvider>
  )
}