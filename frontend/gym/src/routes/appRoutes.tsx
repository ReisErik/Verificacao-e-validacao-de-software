import {
    Routes,
    Route
} from "react-router-dom"

import LoginPage from "@/pages/login/login"
import Layout from "@/components/sidebar/layout"
import HomeUser from "@/pages/home/homeUser"
import ChallengePage from "@/pages/challenge/challengePage"
import InvitePage from "@/pages/challenge/invitePage"

export default function AppRoutes() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<Layout />} >
                <Route path="/" element={<HomeUser />} />
                <Route path="/desafios" element={<ChallengePage/>} />
                <Route path="/convites" element= {<InvitePage/>} />
            </Route>
        </Routes>
    )
}