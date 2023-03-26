import { Navigate, Route, Routes, useNavigate } from "react-router-dom";

import Home from "./pages/home";
import Login from "./pages/login";
import { authToken } from "./store/store";

function App() {
	return (
		<Routes>
			<Route path="/" element={authToken ? <Home /> : <Login />} />
			<Route path="/login" element={<Login />} />
		</Routes>
	);
}

export default App;
