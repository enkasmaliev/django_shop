async function sendPostRequest(url, data){
    return await fetch(
        url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    )
    .then(response => response.json())
    .catch((error) => (console.error(error)))
}


sendPostRequest(
    'http://localhost:8000/auth/user/activation',
    {
        uid: "Mw",
        token: "bmnei1-6f0fda0e3583e42bf7928d6bb7400348"
    }
)