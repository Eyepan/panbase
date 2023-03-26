import { authToken, removeAuthToken, setAuthToken } from "../store/store";

import axios from "axios";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
	const navigate = useNavigate();
	function handleSignout() {
		removeAuthToken();
		navigate(0);
	}

	const apiUrl = import.meta.env.VITE_API_URL;
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
		<>
			<div className="text-4xl">Auth Token: {authToken}</div>
			<button className="p-4 text-white bg-black" onClick={handleSignout}>
				Signout
			</button>
		</>
	);
}

export default Home;
