import { Collection } from "../models/collection.model";

function MainContent(props: { collection: Collection }) {
	const { collection } = props;
	return <div>{collection.collection_name}</div>;
}

export default MainContent;
