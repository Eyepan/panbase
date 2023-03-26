import { authToken, setAuthToken } from "../store/store";

import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

let bodyFormData = new FormData();

const apiUrl = import.meta.env.VITE_API_URL;

function Login() {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const navigate = useNavigate();

	function onSubmit(event: { preventDefault: () => void }) {
		event.preventDefault();
		console.log("Auth token", authToken);
		bodyFormData.append("username", username);
		bodyFormData.append("password", password);
		axios({
			method: "post",
			url: apiUrl + "api/admin/login",
			data: bodyFormData,
			headers: { "Content-Type": "multipart/form-data" },
		})
			.then(function (response) {
				setError("");
				console.log(response.data.access_token);
				setAuthToken(response.data.access_token);
				navigate("/");
			})
			.catch(function (error) {
				setError(error.response.data.detail);
			});
	}

	return (
		<div className="h-screen flex items-center justify-center rounded-none">
			<div className="flex flex-row w-3/4 lg:w-1/2 h-1/2 base">
				<div className="w-1/2 flex items-center justify-center text-4xl base-inverted">
					PanBase
				</div>
				<form
					className="flex flex-col items-center w-1/2 justify-center p-4 gap-8"
					onSubmit={onSubmit}
				>
					<h1 className="text-3xl">Admin</h1>
					<input
						type="text"
						className=" p-4 w-5/6"
						placeholder="Username"
						onChange={(e) => {
							setUsername(e.target.value);
						}}
						required
					/>
					<input
						type="password"
						className=" p-4 w-5/6"
						placeholder="Password"
						onChange={(e) => {
							setPassword(e.target.value);
						}}
						required
					/>
					{error && <div className="text-red-500">{error}</div>}
					<button className=" w-5/6 p-4 ">Submit</button>
				</form>
			</div>
		</div>
	);
}

export default Login;
