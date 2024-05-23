const toggleSidebar=document.querySelector(".toggle-sidebar");
const logo =document.querySelector(".logo-box");
const sidebar =document.querySelector(".sidebar");
const cancel =document.querySelector(".cancel");
const submit=document.querySelector(".submit-button")

const fileInput = document.getElementById('upload');
const uploadButton = document.querySelector('.upload-button');
let load = 0;
let proces;

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  const filename = file.name;
  const extension = filename.split('.').pop();
  let filesize = file.size;

  if (filesize <= 1000000) {
    filesize = (filesize / 1000).toFixed(2) + ' KB';
  } else if (filesize <= 1000000000) {
    filesize = (filesize / 1000000).toFixed(2) + ' MB';
  } else {
    filesize = (filesize / 1000000000).toFixed(2) + ' GB';
  }

  document.querySelector('.upload-label').innerText = filename;
});

uploadButton.addEventListener('click', () => {
  upload();
});

function upload() {
  if (load >= 100) {
    clearInterval(proces);
    uploadButton.classList.remove('active');
  } else {
    load++;
    progress.value = load;
  }
}

uploadButton.onclick = (e) => {
  e.preventDefault();
  uploadButton.classList.add('active');
  uploadButton.style.visibility = 'visible';
  cancel.style.visibility = 'visible';
  submit.style.visibility='visible';
  proces = setInterval(upload, 100);
};

