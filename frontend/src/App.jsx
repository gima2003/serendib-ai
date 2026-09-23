import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Home from "./context/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import { authService } from "./services/authService";

// Planner imports
import PlanTripChoice from "./pages/PlanTripChoice";
import NLPPlanner from "./pages/NLPPlanner";
import GuidedPlanner from "./pages/GuidedPlanner";
import UnifiedReview from "./pages/UnifiedReview";
import TripGeneration from "./pages/TripGeneration";
import TripWorkspace from "./pages/TripWorkspace";

const ProtectedRoute = ({ children }) => {
  const user = authService.getCurrentUser();
  const location = useLocation();
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
};

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <UserDashboard />
          </ProtectedRoute>
        } />
        <Route path="/admin/dashboard" element={
          <ProtectedRoute>
            <AdminDashboard />
          </ProtectedRoute>
        } />
        
        {/* Planner Routes */}
        <Route path="/plan-trip" element={
          <ProtectedRoute>
            <PlanTripChoice />
          </ProtectedRoute>
        } />
        <Route path="/plan-trip/nlp" element={
          <ProtectedRoute>
            <NLPPlanner />
          </ProtectedRoute>
        } />
        <Route path="/plan-trip/guided" element={
          <ProtectedRoute>
            <GuidedPlanner />
          </ProtectedRoute>
        } />
        <Route path="/plan-trip/review" element={
          <ProtectedRoute>
            <UnifiedReview />
          </ProtectedRoute>
        } />
        <Route path="/plan-trip/generating" element={
          <ProtectedRoute>
            <TripGeneration />
          </ProtectedRoute>
        } />
        
        {/* Trip Workspace */}
        <Route path="/trip/:tripId" element={
          <ProtectedRoute>
            <TripWorkspace />
          </ProtectedRoute>
        } />
      </Routes>
    </>
  );
}

export default App;

