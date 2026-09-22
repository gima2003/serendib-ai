import { Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Home from "./context/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";

// Planner imports
import PlanTripChoice from "./pages/PlanTripChoice";
import NLPPlanner from "./pages/NLPPlanner";
import GuidedPlanner from "./pages/GuidedPlanner";
import UnifiedReview from "./pages/UnifiedReview";
import TripGeneration from "./pages/TripGeneration";
import TripWorkspace from "./pages/TripWorkspace";

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<UserDashboard />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        
        {/* Planner Routes */}
        <Route path="/plan-trip" element={<PlanTripChoice />} />
        <Route path="/plan-trip/nlp" element={<NLPPlanner />} />
        <Route path="/plan-trip/guided" element={<GuidedPlanner />} />
        <Route path="/plan-trip/review" element={<UnifiedReview />} />
        <Route path="/plan-trip/generating" element={<TripGeneration />} />
        
        {/* Trip Workspace */}
        <Route path="/trip/:tripId" element={<TripWorkspace />} />
      </Routes>
    </>
  );
}

export default App;
