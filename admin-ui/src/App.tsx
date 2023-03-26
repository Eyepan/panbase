import { Navigate, Route, Routes, useNavigate } from "react-router-dom";

import Login from "./pages/login";
import { authToken } from "./store/store";
import { useEffect } from "react";

function App() {
	const navigate = useNavigate();
	return (
		<Routes>
			<Route
				path="/"
				element={
					authToken ? (
						<Navigate to="/home" />
					) : (
						<Navigate to="/login" />
					)
				}
			/>
			<Route path="/login" element={<Login />} />
		</Routes>
	);
}

export default App;
