function renderImage(formData)
{
    const file = formData.get('Original');
    const $image = document.querySelector('#image_sp');
    const image = URL.createObjectURL(file);
    $image.setAttribute('src', image);



    let img = document.querySelector('#image_sp');
    img.onload = () => {
        let value = img.width > img.height? 500/img.width : 500/img.height;
        let new_width = img.width*value;
        let new_height = img.height*value;
        img.setAttribute('width', new_width);
        img.setAttribute('height', new_height);
    };


}

const $form = document.querySelector('#formData');
const $file = document.querySelector('#Original');
$file.addEventListener('change', (event) => {
    const formData = new FormData($form);
    renderImage(formData);
});

