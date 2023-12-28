function uploadFile(event) {

    event.preventDefault(); // Prevent the default form submission

            const form = document.getElementById('uploadForm');
            const formData = new FormData(form);

            // Fetch presigned URL from the server
            fetch('/upload_files', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                const presignedUrl = data.presigned_url;

                // Perform the actual file upload using the presigned URL
                const xhr = new XMLHttpRequest();
                xhr.open('PUT', presignedUrl, true);
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
        }