import { authToken, removeAuthToken, setAuthToken } from "../store/store";

import { useNavigate } from "react-router-dom";

function Home() {
	const navigate = useNavigate();
	function handleSignout() {
		removeAuthToken();
		navigate(0);
	}

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
