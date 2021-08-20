const subscribeForm = document.getElementById('subscribe-section');
const domain = 'http://localhost:8000'


function myFunction(e) {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    x.innerText = e    // Add the "show" class to DIV
    x.className = "show";    // After 3 seconds, remove the show class from DIV
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
}


subscribeForm.addEventListener('submit', async function (e){
    e.preventDefault();
    let formData = {
        email: subscribeForm.email.value,
    }

    let response = await fetch(domain+window.URLS['subscribeUrl'], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    });

    let responseData = await response.json()
    if (response.ok){
        subscribeForm.email.value = '';
        myFunction('Siz abune oldunuz.')
    }
    else{
        console.log(responseData);
        myFunction(responseData.email)

    }

});


// window.addEventListener("load", async function () {

//        let response = await fetch(domain+window.URLS['recipeDetail'], {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//         },

//     });

//        let responseData = await response.json()
//         if (response.ok){
//             let commenCountElement = document.getElementById('comment-count')
//             commenCountElement.innerText = responseData['comment_count'];
//         }else{
//             alert('Something went wrong');
//         }
// }); 