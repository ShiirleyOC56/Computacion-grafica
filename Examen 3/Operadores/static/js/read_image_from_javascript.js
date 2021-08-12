function readFile(input)
{
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var filePreview = document.createElement('img');
                filePreview.id = 'file-preview';
                filePreview.src = e.target.result;
                var previewZone = document.getElementById('file-preview-zone');
                previewZone.appendChild(filePreview);

            }
            reader.readAsDataURL(input.files[0]);

        }

}

var fileUpload = document.getElementById('file-upload');
fileUpload.onchange = function (e)
{
    readFile(e.srcElement);
}