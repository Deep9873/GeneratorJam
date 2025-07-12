import React from "react";
import "./App.css";
import GeneratorJam from "./components/GeneratorJam";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App">
      <GeneratorJam />
      <Toaster />
    </div>
  );
}

export default App;