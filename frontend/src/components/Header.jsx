import { Link, useLocation } from 'react-router-dom';

function Header() {
  const location = useLocation();
  
  return (
    <header className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 shadow-2xl">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-lg transform hover:rotate-12 transition-transform duration-300">
                <span className="text-3xl">💼</span>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">PeoplePulse</h1>
                <p className="text-sm text-indigo-100 hidden md:block">AI-Powered Attrition Prediction</p>
              </div>
            </div>
          </div>
          <nav className="flex space-x-2">
            <Link
              to="/"
              className={`px-6 py-3 rounded-xl text-sm font-bold transition-all duration-200 transform hover:scale-105 flex items-center space-x-2 ${
                location.pathname === '/' 
                  ? 'bg-white text-indigo-600 shadow-xl' 
                  : 'text-white hover:bg-white hover:bg-opacity-20'
              }`}
            >
              <span className="text-lg">📊</span>
              <span>Dashboard</span>
            </Link>
            <Link
              to="/search"
              className={`px-6 py-3 rounded-xl text-sm font-bold transition-all duration-200 transform hover:scale-105 flex items-center space-x-2 ${
                location.pathname === '/search' 
                  ? 'bg-white text-indigo-600 shadow-xl' 
                  : 'text-white hover:bg-white hover:bg-opacity-20'
              }`}
            >
              <span className="text-lg">🔍</span>
              <span>Employee Search</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header
