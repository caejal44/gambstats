import { createBrowserRouter, type RouteObject } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import ActiveTrip from "./pages/ActiveTrip"
import ActiveSession from "./pages/ActiveSession"
import ActiveGames from "./pages/ActiveGames"
import TripHistory from "./pages/TripHistory";
import GameHistory from "./pages/GameHistory";
import NewGame from "./pages/NewGame";
import NewSession from "./pages/NewSession";
import NewTrip from "./pages/NewTrip";
import SessionHistory from "./pages/SessionHistory";


const routes: RouteObject[] = [
  {
    path: "/",
    element: <Dashboard />,
  },
  {
    path: "/trips/active",
    element: <ActiveTrip />,
  },
  {
    path: "/sessions/active",
    element: <ActiveSession />,
  },
  {
    path: "/games/active",
    element: <ActiveGames />,
  },
  {
    path: "/trips",
    element: <TripHistory />,
  },
  {
    path: "/trips/new",
    element: <NewTrip />,
  },
  {
    path: "/sessions",
    element: <SessionHistory />,
  },
  {
    path: "/sessions/new",
    element: <NewSession />,
  },
  {
    path: "/games",
    element: <GameHistory />,
  },
  {
    path: "/games/new",
    element: <NewGame />,
  },
];
export const router = createBrowserRouter(routes);