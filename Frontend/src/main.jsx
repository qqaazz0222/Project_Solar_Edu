// 라이브러리
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
// 서비스
// 레이아웃
// 페이지
import HomePage from "./pages/home/page";
// 스타일
import "./index.css";
import "./custom.css";

const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />,
    },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
    <RouterProvider router={router} />
);
