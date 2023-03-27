import { Column } from "../models/collection.model";
import axios from "axios";
import { getAuthHeaders } from "../store/store";
import { useState } from "react";

function AddCollectionModal(props: { onClose: any }) {
	const { onClose } = props;
	const [collectionName, setCollectionName] = useState("");
	const [columns, setColumns] = useState<Column[]>([]);
	const [error, setError] = useState("");
	const apiUrl = import.meta.env.VITE_API_URL;

	async function handleAddCollection() {
		const payloadData = {
			collection_name: collectionName,
			columns: columns,
		};
		await axios
			.post(apiUrl + "api/collections", payloadData, getAuthHeaders())
			.then((response) => {
				setError("");
				onClose();
			})
			.catch((error) => {
				setError(error.response.data.detail);
			});
	}

	function handleColumnChange(
		index: number,
		field: keyof Column,
		value: any
	) {
		const updatedColumns: Column[] = [...columns];
		// @ts-ignore
		updatedColumns[index][field] = value; // noqa: ignoring typescript's warnings. i hope i'm doing it right.
		setColumns(updatedColumns);
	}

	function handleAddColumn() {
		setColumns([
			...columns,
			{
				name: "",
				type: "TEXT",
				notnull: false,
				dflt_value: null,
				pk: false,
			},
		]);
	}

	return (
		<div className="w-screen h-screen absolute flex items-center justify-center top-0 left-0 bg-black bg-opacity-50 z-30">
			<div className="md:w-1/2 lg:w-1/3 bg-white z-50 ">
				<form
					onSubmit={(e) => {
						e.preventDefault();
						handleAddCollection();
					}}
					action=""
					className="flex flex-col justify-center h-full p-4 gap-2"
				>
					<div>
						<label htmlFor="">Collection Name</label>
						<input
							type="text"
							className="w-full"
							placeholder="My Collection"
							onChange={(e) => setCollectionName(e.target.value)}
							required
						/>
					</div>
					<label htmlFor="">Columns</label>
					{columns.map((c: Column, index: number) => (
						<div className="flex gap-2" key={index}>
							<input
								type="text"
								className="w-full"
								onChange={(e) =>
									handleColumnChange(
										index,
										"name",
										e.target.value
									)
								}
								required
								value={c.name}
							/>
							<select
								name=""
								id=""
								onChange={(e) =>
									handleColumnChange(
										index,
										"type",
										e.target.value
									)
								}
								required
								value={c.type}
								className="w-1/2 p-4 bg-white border border-black"
							>
								<option value="TEXT">TEXT</option>
								<option value="INTEGER">INTEGER</option>
								<option value="NUMERIC">NUMERIC</option>
								<option value="REAL">REAL</option>
								<option value="BLOB">BLOB</option>
								<option value="DATETIME">DATETIME</option>
							</select>
						</div>
					))}
					<button
						onClick={handleAddColumn}
						className="light-button"
						type="button"
					>
						+
					</button>
					<span className="text-sm">
						System Fields: <code>id</code> of type{" "}
						<code>INTEGER AUTOINCREMENT</code>
					</span>
					{error && <div className="text-red-500">{error}</div>}

					<div className="flex gap-2">
						<button
							type="reset"
							className="light-button hover:bg-neutral-500  w-full"
							onClick={() => {
								onClose();
							}}
						>
							Cancel
						</button>
						<button
							className="dark-button hover:bg-neutral-500 w-full hover:text-white"
							type="submit"
						>
							Add
						</button>
					</div>
				</form>
			</div>
		</div>
	);
}

export default AddCollectionModal;
