document.addEventListener("DOMContentLoaded", () => {
  const addButton = document.getElementById("add");
  const taskInput = document.getElementById("taskInput");
  const taskList = document.getElementById("taskList");

  // Add todo item
  addButton.addEventListener("click", () => {
    const taskText = taskInput.value.trim();
    if (taskText !== "") {
      addTask(taskText);
      taskInput.value = "";
    }
  });

  // Function to create a new task with delete and edit buttons
  function addTask(text) {
    const li = document.createElement("li");
    const span = document.createElement("span");
    span.textContent = text;

    // Edit button
    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.addEventListener("click", () => {
      // Replace span with input
      const editInput = document.createElement("input");
      editInput.type = "text";
      editInput.value = span.textContent;
      li.replaceChild(editInput, span);
      editBtn.style.display = "none";
      saveBtn.style.display = "";

      // Save changes on Save button click or Enter key
      saveBtn.onclick = () => saveEdit();
      editInput.onkeydown = (e) => {
        if (e.key === "Enter") saveEdit();
      };

      function saveEdit() {
        span.textContent = editInput.value.trim() || text;
        li.replaceChild(span, editInput);
        editBtn.style.display = "";
        saveBtn.style.display = "none";
      }
    });

    // Save button for editing (hidden by default)
    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save";
    saveBtn.style.display = "none";

    // Delete button
    const delBtn = document.createElement("button");
    delBtn.textContent = "Delete";
    delBtn.addEventListener("click", () => {
      li.remove();
    });

    li.appendChild(span);
    li.appendChild(editBtn);
    li.appendChild(saveBtn);
    li.appendChild(delBtn);
    taskList.appendChild(li);
  }
});
