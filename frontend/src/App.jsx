import './App.css'
// pages
import AdminDashboard from './pages/AdminDashbord'
// tools
import {Toaster} from 'react-hot-toast';

function App() {

  return (
    <>
      <Toaster position="top-center"/>
      <AdminDashboard/>
    </>
  )
}

export default App
