document.getElementById("submit").addEventListener("click", (e) => {
  e.preventDefault();
  add();
});

function add() {
  const textInput = document.getElementById("text");
  const ol = document.getElementById("ol");

  const text = textInput.value.trim();
  if (text === "") return;

  const li = document.createElement("li");

  const span = document.createElement("span");
  span.textContent = text;

  const input = document.createElement("input");
  input.type = "text";
  input.value = text;
  input.style.display = "none";

  const editBtn = document.createElement("button");
  editBtn.textContent = "Edit";

  const delBtn = document.createElement("button");
  delBtn.textContent = "Delete";

  // Add elements to li
  li.appendChild(span);
  li.appendChild(input);
  li.appendChild(editBtn);
  li.appendChild(delBtn);
  ol.appendChild(li);

  textInput.value = ""; // clear input

  // Delete logic
  delBtn.addEventListener("click", () => {
    li.remove();
  });

  // Edit logic
  editBtn.addEventListener("click", () => {
    if (input.style.display === "none") {
      // Enter edit mode
      span.style.display = "none";
      input.style.display = "inline-block";
      input.focus();
      editBtn.textContent = "Save";
    } else {
      // Save changes
      const newValue = input.value.trim();
      if (newValue !== "") {
        span.textContent = newValue;
      }
      input.style.display = "none";
      span.style.display = "inline";
      editBtn.textContent = "Edit";
    }
  });
}
