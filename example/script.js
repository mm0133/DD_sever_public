const callApi = async () => {
    console.log("wow");
    const url = 'http://127.0.0.1:8000/api/v1/users/my_profile/';
    const responseJson = await fetch(url, {
        headers: {
            Authorization: "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk3Mzc0NDM4LCJqdGkiOiJlMTA2MmU4MzExMGM0MmFlOWQ1ZjYwOGQ2NDM1N2NhMCIsInVzZXJfaWQiOjZ9.JPeduc_cSKIdLdQ5WzOC4h6nAgTFKYS4PijAMYRZxvU",
        },
    }).then(response => response.json())
    console.log(responseJson)
    console.log(responseJson.image)
    document.getElementById('hello').setAttribute('src', `http://127.0.0.1:8000${responseJson.image}`)
}
console.log("wow")
window.onload = callApi;