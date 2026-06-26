import { createBrowserRouter, type RouteObject } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import EditTrip from "./pages/EditTrip"
import EditSession from "./pages/EditSession"
import EditGames from "./pages/EditGames"
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
    path: "/trips/edit",
    element: <EditTrip />,
  },
  {
    path: "/sessions/edit",
    element: <EditSession />,
  },
  {
  path: "/games/:gameId/edit",
  element: <EditGames />,
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