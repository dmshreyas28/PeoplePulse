import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import EmployeeDetail from './pages/EmployeeDetail'
import EmployeeSearch from './pages/EmployeeSearch'
import Header from './components/Header'

function App() {
  return (
    <div className="app">
      <Header />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/employee/:id" element={<EmployeeDetail />} />
        <Route path="/search" element={<EmployeeSearch />} />
      </Routes>
    </div>
  )
}

export default App
