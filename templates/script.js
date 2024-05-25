function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
  
    if (!file) {
      alert('Seleziona un file da caricare');
      return;
    }
  
    var formData = new FormData();
    formData.append('file', file);
  
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
  
    xhr.upload.onprogress = function(e) {
      if (e.lengthComputable) {
        var progress = (e.loaded / e.total) * 100;
        document.getElementById('progress').innerText = 'Progresso: ' + Math.round(progress) + '%';
      }
    };
  
    xhr.onload = function() {
      if (xhr.status === 200) {
        document.getElementById('progress').innerText = 'Caricamento completato!';
      } else {
        document.getElementById('progress').innerText = 'Errore durante il caricamento';
      }
    };
  
    xhr.send(formData);
  }
  