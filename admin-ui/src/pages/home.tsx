import { getAuthHeaders, removeAuthToken } from "../store/store";
import { useEffect, useState } from "react";

import axios from "axios";
import { useNavigate } from "react-router-dom";

function Home() {
	const apiUrl = import.meta.env.VITE_API_URL;
	const [showAddCollection, setShowAddCollection] = useState(false);
	const [collections, setCollections] = useState<string[]>([]);
	const navigate = useNavigate();
	const handleAddCollection = () => {
		console.log("handle add collection");
	};
	const handleSignout = () => {
		removeAuthToken();
		navigate(0);
	};

	useEffect(() => {
		const verifyToken = async () => {
			try {
				const response = await axios.get(
					apiUrl + "verify",
					getAuthHeaders()
				);
				if (!response) {
					navigate("/login");
				}
			} catch (error) {
				console.log(error);
			}
		};
		const getCollections = async () => {
			try {
				const response = await axios.get(
					apiUrl + "api/collections/all",
					getAuthHeaders()
				);
				setCollections(response.data);
			} catch (error) {}
		};
		verifyToken();
		getCollections();
	}, []);

	return (
		<>
			{showAddCollection && (
				<div className="w-screen h-screen absolute flex items-center justify-center top-0 left-0 bg-black bg-opacity-50 z-30">
					<div className="md:w-1/2 lg:w-1/3  bg-white z-50">
						<form
							action=""
							className="flex flex-col justify-center h-full p-4 gap-2"
						>
							<div>
								<label htmlFor="">Collection Name</label>
								<input
									type="text"
									className="w-full"
									placeholder="My Collection"
								/>
							</div>
							<span className="text-sm">
								By default, the columns that are created are
								ID(AUTOINCREMENT)
							</span>
							<div className="flex gap-2">
								<button
									type="reset"
									className="light-button hover:bg-neutral-500  w-full"
									onClick={() => {
										setShowAddCollection(false);
									}}
								>
									Cancel
								</button>
								<button
									className="dark-button hover:bg-neutral-500 w-full"
									type="reset"
									onClick={handleAddCollection}
								>
									Add
								</button>
							</div>
						</form>
					</div>
				</div>
			)}
			<div className="flex">
				<div
					id="SIDEBAR"
					className="h-screen md:w-1/4 lg:w-1/6 flex relative flex-col"
				>
					<div className="p-4 text-center">Collections</div>
					{collections.map((e) => (
						<button className="p-4 my-2 light-button">{e}</button>
					))}
					<button
						className="p-4 my-2 light-button border-dashed"
						onClick={() => {
							setShowAddCollection(true);
						}}
					>
						ADD +
					</button>
					<button
						className="absolute bottom-0 w-full dark-button"
						onClick={handleSignout}
					>
						Signout
					</button>
				</div>
				<div id="MAINCONTENT" className="h-screen md:w-3/4 lg:w-5/6">
					MAIN CONTENT SUCKERS
				</div>
			</div>
		</>
	);
}

export default Home;
