import { Navigate, Route, Routes, useNavigate } from "react-router-dom";

import Home from "./pages/home";
import Login from "./pages/login";
import { authToken } from "./store/store";
import axios from "axios";
import { useEffect } from "react";

const apiUrl = import.meta.env.VITE_API_URL;
function App() {
	const navigate = useNavigate();
	useEffect(() => {
		const verifyToken = async () => {
			try {
				const response = await axios.get(apiUrl + "verify", {
					headers: { Authorization: `Bearer ${authToken}` },
				});
				if (!response) {
					navigate("/login");
				}
			} catch (error) {
				console.log(error);
			}
		};
		verifyToken();
	}, []);

	return (
		<Routes>
			<Route path="/" element={authToken ? <Home /> : <Login />} />
			<Route path="/login" element={<Login />} />
		</Routes>
	);
}

export default App;
