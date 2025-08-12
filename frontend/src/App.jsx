import './App.css'
// tools
import {Toaster} from 'react-hot-toast';
// routes
import { RouterProvider } from "react-router-dom";
import router from '@/routes/router';
import ErrorBoundary from "@/components/ErrorBoundary";



function App() {

  return (
    <>
      <Toaster position="top-center"/>
      <RouterProvider router={router}/>
    </>
  );
}

export default App
