const recipeEditForm = document.getElementById("recipe-edit") ;


window.addEventListener("load", async function (){
    let response = await fetch(domain+window.URLS['updateRecipe']) ;
    if (response.ok) {
        data = await response.json() ;
        recipeEditForm.title.value = data.title ;
        recipeEditForm.short_description.value = data.short_description ;
        recipeEditForm.description.value = data.description ;
        recipeEditForm.image.files[0] = data.image ;
        recipeEditForm.category.value = data.category ;
        recipeEditForm.tag.value = data.tag ;
    }


})
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


recipeEditForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    let form = e.target;

    let postData = new FormData(form);
    postData.append('title', form.title.value);
    postData.append('short_description', form.short_description.value);
    postData.append('description', form.description.value);
    postData.append('image', form.image.files[0]);
    postData.append('category', form.category.value);
    postData.append('tag', form.tag.value);    
    let response = await fetch(domain + window.URLS['updateRecipe'], {
        headers: {
            'Authorization': `Token ${localStorage.getItem('Token')}`
        },
        method: "PUT",
        body: postData,
    }); 
    data = await response.json();    
    if (response.ok) {
        alert('Recipe edited...')    
    }
    else {
        alert('Something went wrong!')
    }
})