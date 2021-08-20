document.querySelector(".delete-event").addEventListener("click", deleteMethod);

function deleteMethod(e) {
    e.preventDefault();
    let recipeId = e.target.dataset.id
    const deleteMethod = {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('Token')}`
        },
    }
    fetch('http://localhost:8000/az/api/recipes/'+ recipeId, deleteMethod)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(err => console.log(err))

    .then(() => location.reload())

}