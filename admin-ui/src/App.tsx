import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { authToken, getAuthHeaders } from "./store/store";

import Home from "./pages/home";
import Login from "./pages/login";

function App() {
	return (
		<Routes>
			<Route path="/home" element={<Home />} />
			<Route path="/login" element={<Login />} />
		</Routes>
	);
}

export default App;
