export interface Column {
	name: string;
	type: string;
	notnull: boolean;
	dflt_value: string | null;
	pk: boolean;
}

export interface Collection {
	collection_name: string;
	columns: Column[];
	contents: any[];
}
