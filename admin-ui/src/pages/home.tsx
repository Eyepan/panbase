import { getAuthHeaders, removeAuthToken } from "../store/store";
import { useEffect, useState } from "react";

import AddCollectionModal from "../components/AddCollectionModal";
import { Collection } from "../models/collection.model";
import MainContent from "../components/MainContent";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Home() {
	const apiUrl = import.meta.env.VITE_API_URL;
	const [showAddCollection, setShowAddCollection] = useState(false);
	const [collections, setCollections] = useState<string[]>([]);
	const navigate = useNavigate();
	const [currentCollection, setCurrentCollection] = useState("");
	const [currentCollectionData, setCurrentCollectionData] =
		useState<Collection>({
			collection_name: "",
			columns: [],
			contents: [],
		});

	function handleSignout() {
		removeAuthToken();
		navigate(0);
	}

	async function verifyToken() {
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
	}
	async function getCollections() {
		try {
			const response = await axios.get(
				apiUrl + "api/collections/all",
				getAuthHeaders()
			);
			setCollections(response.data);
		} catch (error) {}
	}

	async function getCurrentCollectionData() {
		if (currentCollection) {
			await axios
				.get(
					apiUrl + "api/collections/" + currentCollection,
					getAuthHeaders()
				)
				.then((response) => {
					console.log(response);
					setCurrentCollectionData(response.data);
				})
				.catch((error) => {
					console.log(error);
				});
		}
	}
	// on init
	useEffect(() => {
		verifyToken();
		getCollections();
		setCurrentCollection(collections[0]);
	}, []);
	// on update
	useEffect(() => {
		getCollections();
	}, [showAddCollection]);

	useEffect(() => {
		getCurrentCollectionData();
	}, [currentCollection]);
	return (
		<>
			{showAddCollection && (
				<AddCollectionModal
					onClose={() => {
						setShowAddCollection(false);
					}}
				/>
			)}
			<div className="flex">
				<div
					id="SIDEBAR"
					className="h-screen md:w-1/4 lg:w-1/6 flex relative flex-col p-2 bg-neutral-300 rounded-none"
				>
					<div className="p-4 text-center">Collections</div>
					{collections.map((c) => (
						<button
							key={c}
							onClick={(e) => setCurrentCollection(c)}
							className="p-4  light-button my-1"
						>
							{c}
						</button>
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
						className="absolute left-0 bottom-0 w-full dark-button rounded-none"
						onClick={handleSignout}
					>
						Signout
					</button>
				</div>
				<div id="MAINCONTENT" className="h-screen md:w-3/4 lg:w-5/6">
					<MainContent collection={currentCollectionData} />
				</div>
			</div>
		</>
	);
}

export default Home;
