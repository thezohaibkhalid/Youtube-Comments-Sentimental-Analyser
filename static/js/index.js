let activeSection = "youtube";
let map;
let marker;

function setActiveSection(section) {
  const sections = ["youtube", "googlemaps", "text", "file"];
  sections.forEach((s) => {
    const sectionElement = document.getElementById(`${s}Section`);
    const buttonElement = document.getElementById(`${s}SectionBtn`);
    if (s === section) {
      sectionElement.classList.remove("hidden");
      buttonElement.classList.remove("bg-gray-200", "text-gray-700");
      buttonElement.classList.add(
        `bg-${getButtonColor(s)}-600`,
        "text-white"
      );
      activeSection = section;
    } else {
      sectionElement.classList.add("hidden");
      buttonElement.classList.remove(
        `bg-${getButtonColor(s)}-600`,
        "text-white"
      );
      buttonElement.classList.add("bg-gray-200", "text-gray-700");
    }
  });
  updateFormAction();
}

function getButtonColor(section) {
  switch (section) {
    case "youtube":
      return "red";
    case "googlemaps":
      return "blue";
    case "text":
      return "green";
    case "file":
      return "purple";
    default:
      return "gray";
  }
}

function updateFormAction() {
  const form = document.getElementById("inputForm");
  switch (activeSection) {
    case "youtube":
      form.action = "/youtube";
      break;
    case "googlemaps":
      form.action = "/maps";
      break;
    case "text":
      form.action = "/analyze";
      break;
    case "file":
      form.action = "/upload";
      break;
  }
}

function getYouTubeVideoId(url) {
  const regExp =
    /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  const match = url.match(regExp);
  return match && match[2].length === 11 ? match[2] : null;
}

function embedYouTubeVideo(videoId) {
  const embedUrl = `https://www.youtube.com/embed/${videoId}`;
  document.getElementById("youtubeIframe").src = embedUrl;
  document.getElementById("youtubeEmbed").classList.remove("hidden");
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 0, lng: 0 },
    zoom: 2,
  });
  marker = new google.maps.Marker({
    map: map,
    anchorPoint: new google.maps.Point(0, -29),
  });
}

function showGoogleMaps(placeId) {
  const request = {
    placeId: placeId,
    fields: ["name", "geometry"],
  };

  const service = new google.maps.places.PlacesService(map);
  service.getDetails(request, (place, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      map.setCenter(place.geometry.location);
      map.setZoom(15);
      marker.setPosition(place.geometry.location);
      marker.setVisible(true);
      document
        .getElementById("googlemapsEmbed")
        .classList.remove("hidden");
    }
  });
}

document
  .getElementById("youtubeLink")
  .addEventListener("input", function () {
    const videoId = getYouTubeVideoId(this.value);
    if (videoId) {
      document.getElementById("youtubeVideoId").value = videoId;
      embedYouTubeVideo(videoId);
    } else {
      document.getElementById("youtubeEmbed").classList.add("hidden");
    }
  });

document
  .getElementById("googlemapsInput")
  .addEventListener("input", function () {
    const input = this.value;
    if (input.startsWith("https://")) {
      const url = new URL(input);
      const params = new URLSearchParams(url.search);
      const placeId = params.get("q") || params.get("query");
      if (placeId) {
        showGoogleMaps(placeId);
      }
    } else {
      showGoogleMaps(input);
    }
  });

document
  .getElementById("inputForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const youtubeLink = document.getElementById("youtubeLink").value;
    const googlemapsInput =
      document.getElementById("googlemapsInput").value;
    const textInput = document.getElementById("textInput").value;
    const fileInput = document.getElementById("fileInput").value;

    let isValid = false;

    switch (activeSection) {
      case "youtube":
        isValid = youtubeLink && getYouTubeVideoId(youtubeLink);
        break;
      case "googlemaps":
        isValid = googlemapsInput.trim() !== "";
        break;
      case "text":
        isValid = textInput.trim() !== "";
        break;
      case "file":
        isValid = fileInput !== "";
        break;
    }

    if (isValid) {
      this.submit();
    } else {
      alert("Please provide valid input for the selected section.");
    }
  });

setActiveSection("youtube");
initMap();

document
  .getElementById("youtubeLink")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      document.getElementById("submitBtn").click();
    }
  });

document
  .getElementById("googlemapsInput")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      document.getElementById("submitBtn").click();
    }
  });

document
  .getElementById("textInput")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      document.getElementById("submitBtn").click();
    }
  });