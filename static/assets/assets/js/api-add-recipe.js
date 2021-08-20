const recipeForm = document.getElementById('recipe-form');


recipeForm.addEventListener('submit', async function (e){
    e.preventDefault();
    let formData = new FormData()
        formData.append('title',recipeForm.title.value)
        formData.append('short_description',recipeForm.short_description.value)
        formData.append('image',recipeForm.image.files[0])
        formData.append('description',recipeForm.description.value)
        formData.append('category',recipeForm.category.value)
        formData.append('tag',recipeForm.tag.value)
    
    let response = await fetch(domain+window.URLS['recipeUrl'], {
        method: 'POST',
        headers: {
            // 'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('Token')}`
        },
        body: formData,
    });

    if (response.ok){
        window.location.replace("http://localhost:8000")
    }
});


window.addEventListener("load", async function () {

    let response = await fetch(domain+'/api/tags/');

     if (response.ok){
        let responseData = await response.json();
        let tagSelect = document.getElementById('tag');
        let options = '';
        responseData.forEach(element => {
            options += `<option value='${element.id}'>${element.title}</options>`
        });
        tagSelect.innerHTML = options
     }
}); 


window.addEventListener("load", async function () {

    let response = await fetch(domain+'/api/categories/');

     if (response.ok){
        let responseData = await response.json();
        let categorySelect = document.getElementById('category');
        let options = '';
        responseData.forEach(element => {
            options += `<option value='${element.id}'>${element.title}</options>`
        });
        categorySelect.innerHTML = options
     }
}); 