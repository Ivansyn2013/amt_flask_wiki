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
    var input = document.getElementById()
    var file_input_label = document.getElementById()

}

function show_upload_alert (message, alert){
    var alert_wrapper = document.getElementById("alert_wrapper")
    alert_wrapper.innerHTML = `<div class="alert alert-${alert} alert-dismissible fade show" role="alert">
                                 <span>${message}</span> 
                                  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>
`;
};

function input_filename () {
    var file_input_label = document.getElementById("")
    var input = document.getElementById("file_input")

    file_input_label.innerText = ''
};