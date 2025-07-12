document.getElementById("booking-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());
  const resultDiv = document.getElementById("result");
  resultDiv.textContent = "⏳ Отправка...";
  try {
    const response = await fetch("/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const result = await response.text();
    resultDiv.textContent = result;
  } catch (err) {
    resultDiv.textContent = "❌ Ошибка отправки";
  }
});
