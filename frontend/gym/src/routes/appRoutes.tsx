import {
    Routes,
    Route
} from "react-router-dom"

import LoginPage from "@/components/login"
import Layout from "@/components/Sidebar/sideBar"
import HomeUser from "@/pages/homeUser"

export default function AppRoutes() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<Layout />} >
                <Route path="/" element={<HomeUser />} />
                <Route path="/treinos" element={<h1>Treinos</h1>} />
                <Route path="/dashboard" element={<h1>Dashboard</h1>} />
            </Route>
        </Routes>
    )
}