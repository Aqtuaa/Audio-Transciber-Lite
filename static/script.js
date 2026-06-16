const form = document.getElementById("uploadForm");
const statusText = document.getElementById("status");
const resultBox = document.getElementById("resultBox");
const resultText = document.getElementById("resultText");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("audioFile");
  const file = fileInput.files[0];

  if (!file) {
    statusText.textContent = "Please select a file";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  statusText.textContent = "Processing...";
  resultBox.classList.add("hidden");

  try {
    const res = await fetch("/transcribe", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.error) {
      statusText.textContent = data.error;
      return;
    }

    resultText.textContent = data.text;
    resultBox.classList.remove("hidden");
    statusText.textContent = "Finish Transcribing";
  } catch (err) {
    statusText.textContent = "Error";
  }
});
