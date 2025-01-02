let activeSection = "text";

function setActiveSection(section) {
  activeSection = section;
  updateButtonStyles(section);
  toggleSections(section);
  updateFormAction(section);
  clearOtherInputs(section);
}

function updateButtonStyles(section) {
  document.getElementById('youtubeBtn').className = `flex-1 py-3 px-6 rounded-lg font-semibold transition duration-300 ${
    section === 'youtube' ? 'youtube-gradient text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
  }`;
  document.getElementById('instagramBtn').className = `flex-1 py-3 px-6 rounded-lg font-semibold transition duration-300 ${
    section === 'instagram' ? 'instagram-gradient text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
  }`;
  document.getElementById('textBtn').className = `flex-1 py-3 px-6 rounded-lg font-semibold transition duration-300 ${
    section === 'text' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
  }`;
}

function toggleSections(section) {
  document.getElementById('youtubeSection').classList.toggle('hidden', section !== 'youtube');
  document.getElementById('instagramSection').classList.toggle('hidden', section !== 'instagram');
  document.getElementById('textSection').classList.toggle('hidden', section !== 'text');
}

function updateFormAction(section) {
  const form = document.getElementById('inputForm');
  if (section === 'youtube') {
    form.action = '/youtube';
  } else if (section === 'instagram') {
    form.action = '/instagram';
  } else {
    form.action = '/analyze';
  }
}

function clearOtherInputs(section) {
  if (section !== 'youtube') {
    document.getElementById('youtubeLink').value = '';
    document.getElementById('youtubeIframe').src = '';
    document.getElementById('youtubeEmbed').classList.add('hidden');
  }
  if (section !== 'instagram') {
    document.getElementById('instagramLink').value = '';
    document.getElementById('instagramIframe').src = '';
    document.getElementById('instagramEmbed').classList.add('hidden');
  }
  if (section !== 'text') {
    document.getElementById('textInput').value = '';
  }
}

// Initialize default section
setActiveSection('text');

// YouTube Link Input Handling
document.getElementById('youtubeLink').addEventListener('input', function() {
  const youtubeLink = this.value;
  const videoId = extractYoutubeVideoId(youtubeLink);
  if (videoId) {
    document.getElementById('youtubeEmbed').classList.remove('hidden');
    document.getElementById('youtubeIframe').src = `https://www.youtube.com/embed/${videoId}`;
  } else {
    document.getElementById('youtubeEmbed').classList.add('hidden');
    document.getElementById('youtubeIframe').src = '';
  }
});

function extractYoutubeVideoId(url) {
  const regex = /(?:https?:\/\/(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=))|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
  const match = url.match(regex);
  return match ? match[1] : null;
}

// Instagram Link Input Handling
document.getElementById('instagramLink').addEventListener('input', function() {
  const instagramLink = this.value;
  const postId = extractInstagramPostId(instagramLink);
  if (postId) {
    document.getElementById('instagramEmbed').classList.remove('hidden');
    document.getElementById('instagramIframe').src = `https://www.instagram.com/p/${postId}/embed`;
  } else {
    document.getElementById('instagramEmbed').classList.add('hidden');
    document.getElementById('instagramIframe').src = '';
  }
});

function extractInstagramPostId(url) {
  const regex = /(?:https?:\/\/(?:www\.)?instagram\.com\/p\/([a-zA-Z0-9_-]+)\/)/;
  const match = url.match(regex);
  return match ? match[1] : null;
}
