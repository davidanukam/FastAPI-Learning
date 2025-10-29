import React, { useState } from "react";

const AddTaskForm = ({ addTask }) => {
  const [taskName, setTaskName] = useState("");
  const [taskDescription, setTaskDes] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    if (taskName && taskDescription) {
      addTask(taskName, taskDescription);
      setTaskName("");
      setTaskDes("");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
        placeholder="Enter task name"
      />
      <input
        type="text"
        value={taskDescription}
        onChange={(e) => setTaskDes(e.target.value)}
        placeholder="Enter task decription"
      />
      <div>
        <input
          type="radio"
          id="high"
          name="drone"
          value="high"
          defaultChecked
        />
        <label htmlFor="high">High</label>
      </div>
      <div>
        <input type="radio" id="medium" name="drone" value="medium" />
        <label htmlFor="medium">Medium</label>
      </div>
      <div>
        <input type="radio" id="low" name="drone" value="low" />
        <label htmlFor="low">Low</label>
      </div>
      <button type="submit">Add Task</button>
    </form>
  );
};

export default AddTaskForm;
