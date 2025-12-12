import { useState } from 'react';
import { predictEmployee } from '../api';

const EmployeeSearch = () => {
  const [searchType, setSearchType] = useState('number');
  const [searchValue, setSearchValue] = useState('');
  const [employees, setEmployees] = useState([]);
  const [predictions, setPredictions] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Sample employees from dataset (you can expand this)
  const sampleEmployees = [
    { employeeNumber: 1, age: 41, department: 'Sales', jobRole: 'Sales Executive', yearsAtCompany: 6, monthlyIncome: 5993, overtime: 'Yes' },
    { employeeNumber: 2, age: 49, department: 'Research & Development', jobRole: 'Research Scientist', yearsAtCompany: 10, monthlyIncome: 5130, overtime: 'No' },
    { employeeNumber: 4, age: 37, department: 'Research & Development', jobRole: 'Laboratory Technician', yearsAtCompany: 7, monthlyIncome: 2090, overtime: 'Yes' },
    { employeeNumber: 5, age: 33, department: 'Research & Development', jobRole: 'Research Scientist', yearsAtCompany: 8, monthlyIncome: 2909, overtime: 'Yes' },
    { employeeNumber: 7, age: 27, department: 'Research & Development', jobRole: 'Laboratory Technician', yearsAtCompany: 2, monthlyIncome: 2808, overtime: 'Yes' },
  ];

  const handleSearch = () => {
    setError(null);
    let filtered = [];

    if (searchType === 'number') {
      const num = parseInt(searchValue);
      filtered = sampleEmployees.filter(e => e.employeeNumber === num);
    } else if (searchType === 'department') {
      filtered = sampleEmployees.filter(e => 
        e.department.toLowerCase().includes(searchValue.toLowerCase())
      );
    } else if (searchType === 'role') {
      filtered = sampleEmployees.filter(e => 
        e.jobRole.toLowerCase().includes(searchValue.toLowerCase())
      );
    }

    if (filtered.length === 0) {
      setError('No employees found. Try: 1, 2, 4, 5, or 7');
    }

    setEmployees(filtered);
    setPredictions({});
  };

  const handlePredict = async (employee) => {
    setLoading(true);
    setError(null);

    try {
      const requestData = {
        employee_id: `EMP${employee.employeeNumber}`,
        age: employee.age,
        gender: 'Male',
        department: employee.department,
        job_role: employee.jobRole,
        education: 3,
        education_field: 'Life Sciences',
        years_at_company: employee.yearsAtCompany,
        years_in_current_role: Math.floor(employee.yearsAtCompany / 2),
        years_since_last_promotion: 1,
        years_with_curr_manager: Math.floor(employee.yearsAtCompany / 2),
        num_companies_worked: 3,
        monthly_income: employee.monthlyIncome,
        percent_salary_hike: 13,
        stock_option_level: 0,
        training_times_last_year: 2,
        job_satisfaction: 3,
        work_life_balance: 3,
        environment_satisfaction: 3,
        relationship_satisfaction: 3,
        performance_rating: 3,
        business_travel: 'Travel_Rarely',
        distance_from_home: 10,
        marital_status: 'Married',
        overtime: employee.overtime,
        daily_rate: 800,
        hourly_rate: 65,
        monthly_rate: 14000,
        job_level: 2,
        job_involvement: 3,
        total_working_years: employee.yearsAtCompany + 2,
      };

      const response = await predictEmployee(requestData);
      
      setPredictions(prev => ({
        ...prev,
        [employee.employeeNumber]: response
      }));
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate prediction');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'High': return 'bg-red-100 text-red-800 border-red-300';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Low': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header with gradient */}
        <div className="mb-8 text-center">
          <div className="inline-block">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
              Employee Search & Prediction
            </h1>
            <div className="h-1 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-full"></div>
          </div>
          <p className="text-gray-600 mt-4 text-lg">Search for specific employees and predict their attrition risk with AI</p>
        </div>

        {/* Search Section with gradient border */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border-t-4 border-gradient-to-r from-indigo-500 to-purple-500">
          <div className="flex items-center mb-6">
            <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center mr-3">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Search Employees</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="group">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Search By
              </label>
              <select
                value={searchType}
                onChange={(e) => setSearchType(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 bg-gray-50 hover:bg-white"
              >
                <option value="number">🔢 Employee Number</option>
                <option value="department">🏢 Department</option>
                <option value="role">💼 Job Role</option>
              </select>
            </div>

            <div className="group">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                {searchType === 'number' ? 'Employee Number' : searchType === 'department' ? 'Department Name' : 'Job Role'}
              </label>
              <input
                type="text"
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder={searchType === 'number' ? 'e.g., 1, 2, 4, 5, 7' : searchType === 'department' ? 'e.g., Sales' : 'e.g., Sales Executive'}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 bg-gray-50 hover:bg-white"
              />
            </div>

            <div className="flex items-end">
              <button
                onClick={handleSearch}
                className="w-full px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                🔍 Search
              </button>
            </div>
          </div>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg text-red-700 flex items-center animate-shake">
              <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span className="font-medium">{error}</span>
            </div>
          )}
        </div>

        {/* Results Section */}
        {employees.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8 border-t-4 border-gradient-to-r from-purple-500 to-pink-500">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-800">
                Found {employees.length} Employee{employees.length !== 1 ? 's' : ''}
              </h2>
            </div>

            <div className="space-y-6">
              {employees.map((employee) => {
                const prediction = predictions[employee.employeeNumber];

                return (
                  <div key={employee.employeeNumber} className="border-2 border-gray-100 rounded-2xl p-6 hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-white to-gray-50">
                    <div className="flex justify-between items-start mb-6">
                      <div>
                        <div className="flex items-center mb-2">
                          <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-full flex items-center justify-center mr-4">
                            <span className="text-white font-bold text-lg">#{employee.employeeNumber}</span>
                          </div>
                          <div>
                            <h3 className="text-xl font-bold text-gray-900">
                              Employee #{employee.employeeNumber}
                            </h3>
                            <p className="text-indigo-600 font-semibold">{employee.jobRole}</p>
                          </div>
                        </div>
                        <p className="text-sm text-gray-500 ml-16 flex items-center">
                          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clipRule="evenodd" />
                          </svg>
                          {employee.department}
                        </p>
                      </div>
                      <button
                        onClick={() => handlePredict(employee)}
                        disabled={loading}
                        className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                      >
                        {loading ? '🔄 Predicting...' : '🎯 Predict Attrition'}
                      </button>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-xl border border-blue-200">
                        <div className="flex items-center mb-1">
                          <span className="text-2xl mr-2">👤</span>
                          <span className="text-xs text-gray-600 font-semibold">Age</span>
                        </div>
                        <span className="text-2xl font-bold text-blue-700">{employee.age}</span>
                      </div>
                      <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-xl border border-green-200">
                        <div className="flex items-center mb-1">
                          <span className="text-2xl mr-2">📅</span>
                          <span className="text-xs text-gray-600 font-semibold">Years</span>
                        </div>
                        <span className="text-2xl font-bold text-green-700">{employee.yearsAtCompany}</span>
                      </div>
                      <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-xl border border-purple-200">
                        <div className="flex items-center mb-1">
                          <span className="text-2xl mr-2">💰</span>
                          <span className="text-xs text-gray-600 font-semibold">Income</span>
                        </div>
                        <span className="text-xl font-bold text-purple-700">${(employee.monthlyIncome/1000).toFixed(1)}K</span>
                      </div>
                      <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-xl border border-orange-200">
                        <div className="flex items-center mb-1">
                          <span className="text-2xl mr-2">⏰</span>
                          <span className="text-xs text-gray-600 font-semibold">Overtime</span>
                        </div>
                        <span className={`text-xl font-bold ${employee.overtime === 'Yes' ? 'text-orange-700' : 'text-green-700'}`}>
                          {employee.overtime}
                        </span>
                      </div>
                    </div>

                    {prediction && (
                      <div className="mt-6 pt-6 border-t-2 border-gray-200">
                        <div className="flex items-center justify-between mb-6">
                          <div className="flex items-center">
                            <span className="text-3xl mr-3">🎯</span>
                            <h4 className="text-xl font-bold text-gray-900">AI Prediction Result</h4>
                          </div>
                          <span className={`px-6 py-3 rounded-full text-base font-bold border-2 shadow-lg ${getRiskColor(prediction.risk_level)}`}>
                            {prediction.risk_level} Risk
                          </span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-6 rounded-2xl border-2 border-indigo-200">
                            <div className="flex items-center mb-3">
                              <span className="text-2xl mr-2">📊</span>
                              <p className="text-sm font-semibold text-gray-700">Attrition Probability</p>
                            </div>
                            <div className="flex items-center">
                              <div className="flex-1 bg-gray-200 rounded-full h-4 mr-4 shadow-inner">
                                <div
                                  className={`h-4 rounded-full transition-all duration-1000 ${
                                    prediction.attrition_probability > 0.6 ? 'bg-gradient-to-r from-red-500 to-red-600' :
                                    prediction.attrition_probability > 0.3 ? 'bg-gradient-to-r from-yellow-500 to-orange-500' :
                                    'bg-gradient-to-r from-green-500 to-green-600'
                                  }`}
                                  style={{ width: `${prediction.attrition_probability * 100}%` }}
                                />
                              </div>
                              <span className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                                {(prediction.attrition_probability * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>

                          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-6 rounded-2xl border-2 border-blue-200">
                            <div className="flex items-center mb-3">
                              <span className="text-2xl mr-2">✅</span>
                              <p className="text-sm font-semibold text-gray-700">Model Confidence</p>
                            </div>
                            <p className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                              {(prediction.confidence * 100).toFixed(1)}%
                            </p>
                          </div>
                        </div>

                        {prediction.top_factors && prediction.top_factors.length > 0 && (
                          <div className="bg-gradient-to-br from-yellow-50 to-orange-50 p-6 rounded-2xl border-2 border-yellow-200 mb-6">
                            <div className="flex items-center mb-4">
                              <span className="text-2xl mr-2">🔍</span>
                              <p className="text-lg font-bold text-gray-800">Top Risk Factors</p>
                            </div>
                            <div className="space-y-3">
                              {prediction.top_factors.slice(0, 3).map((factor, idx) => (
                                <div key={idx} className="flex items-center bg-white p-4 rounded-xl shadow-md hover:shadow-lg transition-shadow">
                                  <span className="w-8 h-8 rounded-full bg-gradient-to-r from-yellow-400 to-orange-400 text-white font-bold flex items-center justify-center text-sm mr-4 shadow">
                                    {idx + 1}
                                  </span>
                                  <span className="text-gray-800 font-semibold flex-1">{factor.feature}</span>
                                  <span className={`px-4 py-2 rounded-lg font-bold ${factor.impact > 0 ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                                    {factor.impact > 0 ? '+' : ''}{factor.impact.toFixed(3)}
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {prediction.recommendation && (
                          <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-6 rounded-2xl shadow-xl">
                            <div className="flex items-start text-white">
                              <span className="text-3xl mr-4">💡</span>
                              <div>
                                <p className="font-bold text-lg mb-2">Recommendation</p>
                                <p className="text-blue-50 leading-relaxed">{prediction.recommendation}</p>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Info Box */}
        <div className="mt-8 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 rounded-2xl shadow-2xl p-1">
          <div className="bg-white rounded-xl p-6">
            <div className="flex items-center mb-3">
              <span className="text-3xl mr-3">💡</span>
              <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Quick Start Guide
              </h3>
            </div>
            <p className="text-gray-700 leading-relaxed">
              Try searching: <span className="inline-flex items-center px-3 py-1 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-lg font-mono font-bold text-indigo-700 mx-1">1, 2, 4, 5, 7</span> 
              or filter by Department: <span className="inline-flex items-center px-3 py-1 bg-gradient-to-r from-blue-100 to-cyan-100 rounded-lg font-semibold text-blue-700 mx-1">Sales, Research & Development</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmployeeSearch;
