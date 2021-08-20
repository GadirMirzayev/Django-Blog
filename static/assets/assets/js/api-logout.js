const logout = document.getElementById('log_out');

logout.addEventListener('click', async function (e){
    let response = await fetch(domain+'/en/accounts/logout/' ,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
     });
        localStorage.removeItem('Token');
        window.location.replace("http://localhost:8000")

});