let activeSection = 'youtube';

function setActiveSection(section) {
  const sections = ['youtube', 'googlemaps', 'text', 'file'];
  sections.forEach(s => {
    const sectionElement = document.getElementById(`${s}Section`);
    const buttonElement = document.getElementById(`${s}SectionBtn`);
    if (s === section) {
      sectionElement.classList.remove('hidden');
      buttonElement.classList.remove('bg-gray-200', 'text-gray-700');
      buttonElement.classList.add('bg-blue-500', 'text-white');
      activeSection = section;
    } else {
      sectionElement.classList.add('hidden');
      buttonElement.classList.remove('bg-blue-500', 'text-white');
      buttonElement.classList.add('bg-gray-200', 'text-gray-700');
    }
  });
  updateFormAction();
}

function updateFormAction() {
  const form = document.getElementById('inputForm');
  switch (activeSection) {
    case 'youtube':
      form.action = '/youtube';
      break;
    case 'googlemaps':
      form.action = '/maps';
      break;
    case 'text':
      form.action = '/analyze';
      break;
    case 'file':
      form.action = '/upload';
      break;
  }
}

function getYouTubeVideoId(url) {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
}

function embedYouTubeVideo(videoId) {
  const embedUrl = `https://www.youtube.com/embed/${videoId}`;
  document.getElementById('youtubeIframe').src = embedUrl;
  document.getElementById('youtubeEmbed').classList.remove('hidden');
}

function isValidGoogleMapsUrl(url) {
  return url.startsWith('https://www.google.com/maps/embed') || url.startsWith('https://goo.gl/maps/');
}

function embedGoogleMaps(url) {
  let embedUrl = url;
  if (url.startsWith('https://goo.gl/maps/')) {
     embedUrl = `https://www.google.com/maps/embed?pb=${url.split('/').pop()}`;
  }
  document.getElementById('googlemapsIframe').src = embedUrl;
  document.getElementById('googlemapsEmbed').classList.remove('hidden');
}

document.getElementById('youtubeLink').addEventListener('input', function() {
  const videoId = getYouTubeVideoId(this.value);
  if (videoId) {
    document.getElementById('youtubeVideoId').value = videoId;
    embedYouTubeVideo(videoId);
  } else {
    document.getElementById('youtubeEmbed').classList.add('hidden');
  }
});

document.getElementById('googlemapsLink').addEventListener('input', function() {
  if (isValidGoogleMapsUrl(this.value)) {
    embedGoogleMaps(this.value);
  } else {
    document.getElementById('googlemapsEmbed').classList.add('hidden');
  }
});

document.getElementById('inputForm').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const youtubeLink = document.getElementById('youtubeLink').value;
  const googlemapsLink = document.getElementById('googlemapsLink').value;
  const textInput = document.getElementById('textInput').value;
  const fileInput = document.getElementById('fileInput').value;

  let isValid = false;

  switch (activeSection) {
    case 'youtube':
      isValid = youtubeLink && getYouTubeVideoId(youtubeLink);
      break;
    case 'googlemaps':
      isValid = googlemapsLink && isValidGoogleMapsUrl(googlemapsLink);
      break;
    case 'text':
      isValid = textInput.trim() !== '';
      break;
    case 'file':
      isValid = fileInput !== '';
      break;
  }

  if (isValid) {
    this.submit();
  } else {
    this.submit();
   }
});

 setActiveSection('youtube');

 document.getElementById('youtubeLink').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    document.getElementById('submitBtn').click();
  }
});

document.getElementById('googlemapsLink').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    document.getElementById('submitBtn').click();
  }
});

document.getElementById('textInput').addEventListener('keypress', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    document.getElementById('submitBtn').click();
  }
});

