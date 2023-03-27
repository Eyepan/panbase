import { Collection } from "../models/collection.model";

function MainContent(props: { collection: Collection }) {
	const { collection } = props;
	return (
		<>
			<div>{collection.collection_name}</div>
			<div className="">
				{collection.columns.map((c) => (
					<div>
						{c.name} {c.type}
					</div>
				))}
			</div>
		</>
	);
}

export default MainContent;
