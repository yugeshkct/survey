const questionsContainer = document.getElementById("questionsContainer");
const addQuestionBtn = document.getElementById("addQuestionBtn");
const surveyForm = document.getElementById("surveyForm");
const responseBox = document.getElementById("responseBox");
const responseMessage = document.getElementById("responseMessage");
const surveyLink = document.getElementById("surveyLink");

// Change this to your backend VM IP
const BACKEND_URL = "http://23.20.227.42:5000/api/create-survey";

let questionCount = 0;

function addQuestionBlock() {
  questionCount++;

  const block = document.createElement("div");
  block.className = "question-block";
  block.innerHTML = `
    <h3>Question ${questionCount}</h3>
    <label>Question Title</label>
    <input type="text" class="question-title" placeholder="e.g. Work life balance" required />

    <label>Question Description</label>
    <input type="text" class="question-description" placeholder="Enter question description" required />

    <label>Answer Choices (comma separated)</label>
    <input type="text" class="question-answers" placeholder="Yes,No,Maybe" required />
  `;

  questionsContainer.appendChild(block);
}

addQuestionBtn.addEventListener("click", addQuestionBlock);

// Add one question by default
addQuestionBlock();

surveyForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const surveyName = document.getElementById("surveyName").value.trim();
  const pageName = document.getElementById("pageName").value.trim();

  const questionBlocks = document.querySelectorAll(".question-block");
  const questions = {};

  questionBlocks.forEach((block) => {
    const title = block.querySelector(".question-title").value.trim();
    const description = block.querySelector(".question-description").value.trim();
    const answers = block.querySelector(".question-answers").value
      .split(",")
      .map(a => a.trim())
      .filter(a => a);

    questions[title] = {
      Description: description,
      Answers: answers
    };
  });

  const payload = {
    [surveyName]: {
      [pageName]: questions
    }
  };

  try {
    const res = await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    responseBox.classList.remove("hidden");

    if (res.ok) {
      responseMessage.textContent = data.message || "Survey created successfully.";
      surveyLink.href = data.survey_link;
      surveyLink.textContent = data.survey_link;
    } else {
      responseMessage.textContent = data.error || "Failed to create survey.";
      surveyLink.textContent = "";
    }
  } catch (error) {
    responseBox.classList.remove("hidden");
    responseMessage.textContent = "Error connecting to backend.";
    surveyLink.textContent = "";
  }
});
