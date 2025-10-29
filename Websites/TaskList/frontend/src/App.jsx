import React from "react";
import "./App.css";
import TaskList from "./components/Tasks";

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Task List</h1>
      </header>
      <main>
        <TaskList />
      </main>
    </div>
  );
};

export default App;
