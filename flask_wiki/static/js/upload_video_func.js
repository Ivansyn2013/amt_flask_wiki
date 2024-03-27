function getURL()    {
    const pathname = window.location.pathname;

    // Split the pathname by '/' to get an array of parts
    const urlParts = pathname.split('/');

    // Remove any empty parts resulting from leading or trailing slashes
    const cleanUrlParts = urlParts.filter(part => part !== '');

    // Get the last part of the URL
    const lastPart = cleanUrlParts[cleanUrlParts.length - 1];

    return lastPart;
};


function uploadFileProgress() {
    var input = document.getElementById("file_input")
    var progress = document.getElementById("progress");
    var progress_wrapper = document.getElementById("progress_wrapper");
    var progress_status = document.getElementById("progress_status");

    var upload_btn = document.getElementById("upload_btn");
    var cancel_btn = document.getElementById("cancel_btn");
    var loadding_btn = document.getElementById("loadding_btn");

    var alert_wrapper = document.getElementById("alert_wrapper")
    var file_input_label = document.getElementById("file_input_label")
    const pagename = getURL();

    if (!input.value) {
        show_upload_alert("Фаил не выбран", "warning");
        return;
    }

    let data = new FormData();
    let request = new XMLHttpRequest();
    request.responseType = "json"

    alert_wrapper.innerHTML = ''
    input.disabled = true;
    upload_btn.classList.add("d-none")
    loadding_btn.classList.remove("d-none")
    cancel_btn.classList.remove("d-none")
    progress_wrapper.classList.remove("d-none")

    let file = input.files[0];
    let filename = file.name;
    let filesize = file.size;

    document.cooke = `filesize=${filesize}`;

    data.append("file", file)

    request.upload.addEventListener("progress", function (event){
        let loaded = event.loaded;
        let total = event.total;
        let percentage_complete = (loaded / total) * 100;

        progress.setAttribute('style', `width: ${Math.floor(percentage_complete)}%`);
        progress_status.innerText = `${Math.floor(percentage_complete)}%`;
    })

    request.addEventListener("load", function (event) {

        if (request.status == 200) {

            show_upload_alert(`${request.response.message}`, "success");
            reset_upload();
        }
        else {
            show_upload_alert("Ошибка загрузки файла", "danger");
            reset_upload();
        }


    })

    request.addEventListener("error", function (event){
        reset_upload();
        show_upload_alert("Ошибка загрузки файла", "danger");

    })

    request.open("post", "/upload_files/");
    request.setRequestHeader("pagename", pagename);
    request.setRequestHeader("full_url", window.location.pathname);

    request.send(data);

    cancel_btn.addEventListener("click", function (event){
        request.abort();
        reset_upload();
    })

 }

function reset_upload(){
    var input = document.getElementById("file_input")
    var upload_btn = document.getElementById("upload_btn");
    var cancel_btn = document.getElementById("cancel_btn");
    var loadding_btn = document.getElementById("loadding_btn");
    var progress_wrapper = document.getElementById("progress_wrapper");
    var progress = document.getElementById("progress");
    var file_input_label = document.getElementById("file_input_label")


    input.value = null;
    input.disabled = false
    cancel_btn.classList.add('d-none');
    loadding_btn.classList.add('d-none');
    upload_btn.classList.remove('d-none');
    progress_wrapper.classList.add('d-none');
    progress.setAttribute("style", "width: 0%");
    file_input_label.innerText = "Выбери фаил";

}


function uploadFile(event) {
    var input = document.getElementById("file_input")

    if (!input.value) {
        show_upload_alert("Фаил не выбран", "warning");
        return;
    }

    event.preventDefault(); // Prevent the default form submission

            const form = document.getElementById('uploadForm');
            const formData = new FormData(form);
            const pagename = getURL()
            const headers = new Headers();

            headers.append('pagename', pagename);
            headers.append('full_url', window.location.pathname);
            // Fetch presigned URL from the server
            fetch('/upload_files/', {
                method: 'POST',
                body: formData,
                headers: headers,
            })
            .then(response =>  response.json())
                .then(data => {

                // Perform the actual file upload using the presigned URL
                const xhr = new XMLHttpRequest();
                xhr.open('PUT', pagename, true);
                xhr.setRequestHeader('Content-Type', formData.get('file').type);

                xhr.upload.onprogress = function (e) {
                    if (e.lengthComputable) {
                        const percent = (e.loaded / e.total) * 100;
                        document.getElementById('progressBarFill').style.width = percent + '%';
                    }
                };

                xhr.onload = function () {
                    if (xhr.status === 200) {
                        // File successfully uploaded
                        document.getElementById('progressBar').style.display = 'none';

                        // Add the uploaded file to the list
                        const uploadedFilesList = document.getElementById('uploadedFiles');
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<a href="${S3_BASE_URL}${file.name}" target="_blank">${S3_BASE_URL}${file.name}</a>`;
                        uploadedFilesList.appendChild(listItem);
                    } else {
                        // Handle error
                        alert('File upload failed. Please try again.');
                    }
                };

                xhr.onerror = function () {
                    alert('Error during file upload. Please try again.');
                };

                document.getElementById('progressBar').style.display = 'block';
                xhr.send(formData.get('file'));
            })
            .catch(error => {
                console.error('Error fetching presigned URL:', error);
                alert('Error fetching presigned URL. Please try again.');
            });
        };

function removeFile(event){
  event.preventDefault();

  const parentAlink = event.target.parentElement.parentElement.parentElement
  const prevAlink = event.target.parentElement.parentElement.parentElement.previousElementSibling
  const filename = event.target.parentElement.parentElement.parentElement.previousElementSibling.getAttribute('data-filename');

  const pagename = getURL();
  const headers = new Headers();

  headers.append('pagename', pagename);
  headers.append('remove_file', filename);

  fetch('/remove_files/', {
      method: 'POST',
      headers: headers,
      body: filename,
  })
      .then(responce => {
          if (!responce.ok) {
              throw new Error('HTTP error')
          }
          return responce.json()
      })
      .then(data => {
          alert(data.message);
          if (data.status === 'success') {
              prevAlink.remove();
              parentAlink.remove();
          }
      })
      .catch(error => {
          console.error(error)
      })


};


function test_progress(){
    var progress = document.getElementById("progress");
    var progress_wrapper = document.getElementById("progress_wrapper");
    var progress_status = document.getElementById("progress_status");

    var upload_btn = document.getElementById("upload_btn");
    var cancel_btn = document.getElementById("cancel_btn");
    var loadding_btn = document.getElementById("loadding_btn");

    var alert_wrapper = document.getElementById("alert_wrapper")
    var input = document.getElementById("file_input")
    var file_input_label = document.getElementById("file_input_label")

}

function show_upload_alert (message, alert){
    var alert_wrapper = document.getElementById("alert_wrapper")
    alert_wrapper.innerHTML = `<div class="alert alert-${alert} alert-dismissible fade show" role="alert">
                ${message}
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>`;
};

function input_filename () {
    var file_input_label = document.getElementById("file_input_label")
    var input = document.getElementById("file_input")

    file_input_label.innerText = input.files[0].name
};