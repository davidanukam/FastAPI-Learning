import React, { useEffect, useState } from "react";
import AddTaskForm from "./AddTaskForm";
import api from "../api";

const TaskList = () => {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    try {
      const response = await api.get("/tasks");
        setTasks(response.data.tasks);
        console.log("WORKED!")
    } catch (error) {
      console.error("Error fetching tasks", error);
    }
  };

  const addTask = async (taskName, taskDes) => {
    try {
      await api.post("/tasks", {
        task_name: taskName,
        task_description: taskDes,
        priority: 3, // optional, defaults to LOW anyway
      });
      fetchTasks(); // Refresh the list after adding a task
    } catch (error) {
      console.error("Error adding task", error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div>
      <h2>Tasks List</h2>
      <ul>
        {tasks?.map((task, index) => (
          <li key={index}>{task.name}</li>
        ))}
      </ul>
      <AddTaskForm addTask={addTask} />
    </div>
  );
};

export default TaskList;
