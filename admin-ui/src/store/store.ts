let authToken = "";
const authTokenCookie = document.cookie.match(/authToken=([^;]+)/);
if (authTokenCookie) {
	authToken = authTokenCookie[1];
	console.log("Found auth token in cookie: ", authToken);
}

function setAuthToken(token: string) {
	authToken = token;
	document.cookie = `authToken=${authToken}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;
	console.log("Auth token set to ", authToken);
}

function removeAuthToken() {
	document.cookie = `authToken=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
}

function getAuthHeaders() {
	return {
		headers: { Authorization: `Bearer ${authToken}` },
	};
}
export { authToken, setAuthToken, removeAuthToken, getAuthHeaders };
