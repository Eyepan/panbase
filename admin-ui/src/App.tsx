import { Navigate, Route, Routes, useNavigate } from "react-router-dom";

import Home from "./pages/home";
import Login from "./pages/login";
import { authToken } from "./store/store";
import { useEffect } from "react";

function App() {
	const navigate = useNavigate();
	useEffect(() => {
		if (authToken == "") {
			navigate("/login");
		} else {
			navigate("/");
		}
	}, [authToken]);

	return (
		<Routes>
			<Route path="/" element={<Home />} />
			<Route path="/login" element={<Login />} />
		</Routes>
	);
}

export default App;
