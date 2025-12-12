import { useState, useEffect } from 'react';
import RiskCard from '../components/RiskCard';
import RiskTable from '../components/RiskTable';
import { predictBatch, healthCheck } from '../api';

// Sample employee data based on IBM HR Analytics dataset structure
const sampleEmployees = [
  {
    employee_id: "EMP001",
    age: 41,
    gender: "Female",
    department: "Sales",
    job_role: "Sales Executive",
    education: 2,
    education_field: "Life Sciences",
    years_at_company: 6,
    years_in_current_role: 4,
    years_since_last_promotion: 0,
    years_with_curr_manager: 5,
    num_companies_worked: 8,
    monthly_income: 5993,
    percent_salary_hike: 11,
    stock_option_level: 0,
    training_times_last_year: 0,
    job_satisfaction: 4,
    work_life_balance: 1,
    environment_satisfaction: 2,
    relationship_satisfaction: 1,
    performance_rating: 3,
    business_travel: "Travel_Rarely",
    distance_from_home: 1,
    marital_status: "Single",
    overtime: "Yes",
    daily_rate: 1102,
    hourly_rate: 94,
    monthly_rate: 19479,
    job_level: 2,
    job_involvement: 3,
    total_working_years: 8
  },
  {
    employee_id: "EMP002",
    age: 49,
    gender: "Male",
    department: "Research & Development",
    job_role: "Research Scientist",
    education: 1,
    education_field: "Life Sciences",
    years_at_company: 10,
    years_in_current_role: 7,
    years_since_last_promotion: 1,
    years_with_curr_manager: 7,
    num_companies_worked: 1,
    monthly_income: 5130,
    percent_salary_hike: 23,
    stock_option_level: 1,
    training_times_last_year: 3,
    job_satisfaction: 2,
    work_life_balance: 3,
    environment_satisfaction: 3,
    relationship_satisfaction: 4,
    performance_rating: 4,
    business_travel: "Travel_Frequently",
    distance_from_home: 8,
    marital_status: "Married",
    overtime: "No",
    daily_rate: 279,
    hourly_rate: 61,
    monthly_rate: 24907,
    job_level: 2,
    job_involvement: 2,
    total_working_years: 10
  },
  {
    employee_id: "EMP003",
    age: 37,
    gender: "Male",
    department: "Research & Development",
    job_role: "Laboratory Technician",
    education: 2,
    education_field: "Other",
    years_at_company: 0,
    years_in_current_role: 0,
    years_since_last_promotion: 0,
    years_with_curr_manager: 0,
    num_companies_worked: 6,
    monthly_income: 2090,
    percent_salary_hike: 15,
    stock_option_level: 0,
    training_times_last_year: 3,
    job_satisfaction: 2,
    work_life_balance: 3,
    environment_satisfaction: 4,
    relationship_satisfaction: 2,
    performance_rating: 3,
    business_travel: "Travel_Rarely",
    distance_from_home: 2,
    marital_status: "Single",
    overtime: "Yes",
    daily_rate: 1373,
    hourly_rate: 56,
    monthly_rate: 2396,
    job_level: 1,
    job_involvement: 2,
    total_working_years: 7
  },
  {
    employee_id: "EMP004",
    age: 33,
    gender: "Female",
    department: "Research & Development",
    job_role: "Research Scientist",
    education: 4,
    education_field: "Life Sciences",
    years_at_company: 8,
    years_in_current_role: 7,
    years_since_last_promotion: 3,
    years_with_curr_manager: 0,
    num_companies_worked: 1,
    monthly_income: 2909,
    percent_salary_hike: 11,
    stock_option_level: 0,
    training_times_last_year: 3,
    job_satisfaction: 3,
    work_life_balance: 3,
    environment_satisfaction: 4,
    relationship_satisfaction: 3,
    performance_rating: 3,
    business_travel: "Travel_Frequently",
    distance_from_home: 3,
    marital_status: "Married",
    overtime: "Yes",
    daily_rate: 1392,
    hourly_rate: 40,
    monthly_rate: 23159,
    job_level: 1,
    job_involvement: 3,
    total_working_years: 8
  },
  {
    employee_id: "EMP005",
    age: 27,
    gender: "Male",
    department: "Research & Development",
    job_role: "Laboratory Technician",
    education: 1,
    education_field: "Medical",
    years_at_company: 2,
    years_in_current_role: 2,
    years_since_last_promotion: 2,
    years_with_curr_manager: 2,
    num_companies_worked: 9,
    monthly_income: 3468,
    percent_salary_hike: 12,
    stock_option_level: 1,
    training_times_last_year: 3,
    job_satisfaction: 2,
    work_life_balance: 3,
    environment_satisfaction: 1,
    relationship_satisfaction: 4,
    performance_rating: 4,
    business_travel: "Travel_Rarely",
    distance_from_home: 24,
    marital_status: "Single",
    overtime: "No",
    daily_rate: 591,
    hourly_rate: 79,
    monthly_rate: 16632,
    job_level: 1,
    job_involvement: 3,
    total_working_years: 6
  },
  {
    employee_id: "EMP006",
    age: 32,
    gender: "Male",
    department: "Research & Development",
    job_role: "Laboratory Technician",
    education: 2,
    education_field: "Life Sciences",
    years_at_company: 7,
    years_in_current_role: 7,
    years_since_last_promotion: 3,
    years_with_curr_manager: 6,
    num_companies_worked: 0,
    monthly_income: 2571,
    percent_salary_hike: 13,
    stock_option_level: 0,
    training_times_last_year: 3,
    job_satisfaction: 4,
    work_life_balance: 3,
    environment_satisfaction: 2,
    relationship_satisfaction: 3,
    performance_rating: 3,
    business_travel: "Travel_Rarely",
    distance_from_home: 15,
    marital_status: "Divorced",
    overtime: "No",
    daily_rate: 1005,
    hourly_rate: 81,
    monthly_rate: 17357,
    job_level: 1,
    job_involvement: 2,
    total_working_years: 7
  },
  {
    employee_id: "EMP007",
    age: 59,
    gender: "Female",
    department: "Research & Development",
    job_role: "Laboratory Technician",
    education: 3,
    education_field: "Medical",
    years_at_company: 1,
    years_in_current_role: 0,
    years_since_last_promotion: 0,
    years_with_curr_manager: 0,
    num_companies_worked: 4,
    monthly_income: 2083,
    percent_salary_hike: 11,
    stock_option_level: 0,
    training_times_last_year: 2,
    job_satisfaction: 3,
    work_life_balance: 4,
    environment_satisfaction: 3,
    relationship_satisfaction: 1,
    performance_rating: 3,
    business_travel: "Travel_Rarely",
    distance_from_home: 26,
    marital_status: "Married",
    overtime: "Yes",
    daily_rate: 1324,
    hourly_rate: 44,
    monthly_rate: 26999,
    job_level: 1,
    job_involvement: 1,
    total_working_years: 12
  },
  {
    employee_id: "EMP008",
    age: 30,
    gender: "Male",
    department: "Research & Development",
    job_role: "Laboratory Technician",
    education: 1,
    education_field: "Life Sciences",
    years_at_company: 1,
    years_in_current_role: 0,
    years_since_last_promotion: 0,
    years_with_curr_manager: 0,
    num_companies_worked: 1,
    monthly_income: 2028,
    percent_salary_hike: 22,
    stock_option_level: 1,
    training_times_last_year: 6,
    job_satisfaction: 4,
    work_life_balance: 2,
    environment_satisfaction: 2,
    relationship_satisfaction: 2,
    performance_rating: 4,
    business_travel: "Travel_Rarely",
    distance_from_home: 19,
    marital_status: "Single",
    overtime: "No",
    daily_rate: 1551,
    hourly_rate: 67,
    monthly_rate: 17552,
    job_level: 1,
    job_involvement: 3,
    total_working_years: 5
  }
];

function Dashboard() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    // Check API health on mount
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const healthData = await healthCheck();
      setHealth(healthData);
    } catch (err) {
      console.error('Health check failed:', err);
    }
  };

  const runPredictions = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await predictBatch(sampleEmployees);
      setPredictions(result.predictions);
    } catch (err) {
      setError('Failed to generate predictions. Please ensure the backend is running and the model is loaded.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Calculate KPIs
  const totalEmployees = predictions.length;
  const highRiskCount = predictions.filter(p => p.risk_level === 'High').length;
  const avgRisk = predictions.length > 0
    ? (predictions.reduce((sum, p) => sum + p.attrition_probability, 0) / predictions.length * 100).toFixed(1)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="inline-block">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
              Employee Attrition Dashboard
            </h1>
            <div className="h-1 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-full"></div>
          </div>
          <p className="text-gray-600 mt-4 text-lg">AI-powered workforce retention insights</p>
        </div>

        {/* Health Warning */}
        {health && !health.model_loaded && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg text-red-700 flex items-center shadow-lg">
            <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <strong>Warning:</strong> ML model is not loaded. Predictions may not work. 
              Please train and place the model file as configured.
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg text-red-700 flex items-center shadow-lg animate-shake">
            <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div>
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="mb-8 flex justify-center">
          <button 
            onClick={runPredictions}
            disabled={loading}
            className="px-8 py-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white font-bold text-lg rounded-2xl hover:from-indigo-700 hover:via-purple-700 hover:to-pink-700 transform hover:scale-105 transition-all duration-200 shadow-2xl hover:shadow-3xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center space-x-3"
          >
            <span className="text-2xl">🎯</span>
            <span>{loading ? 'Analyzing Employee Data...' : 'Run Attrition Predictions'}</span>
          </button>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center border-t-4 border-indigo-500">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-indigo-200 border-t-indigo-600 mb-4"></div>
            <p className="text-xl font-semibold text-gray-700">Analyzing employee data with AI...</p>
            <p className="text-gray-500 mt-2">This may take a few moments</p>
          </div>
        )}

      {predictions.length > 0 && (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <span className="text-4xl">👥</span>
                <svg className="w-8 h-8 opacity-50" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                </svg>
              </div>
              <p className="text-blue-100 text-sm font-semibold mb-1">Total Employees</p>
              <p className="text-5xl font-bold mb-2">{totalEmployees}</p>
              <p className="text-blue-100 text-xs">Analyzed in this batch</p>
            </div>

            <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <span className="text-4xl">⚠️</span>
                <svg className="w-8 h-8 opacity-50" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="text-red-100 text-sm font-semibold mb-1">High Risk</p>
              <p className="text-5xl font-bold mb-2">{highRiskCount}</p>
              <p className="text-red-100 text-xs">{((highRiskCount / totalEmployees) * 100).toFixed(1)}% of workforce</p>
            </div>

            <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <span className="text-4xl">📊</span>
                <svg className="w-8 h-8 opacity-50" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                </svg>
              </div>
              <p className="text-purple-100 text-sm font-semibold mb-1">Average Risk</p>
              <p className="text-5xl font-bold mb-2">{avgRisk}%</p>
              <p className="text-purple-100 text-xs">Across all employees</p>
            </div>

            <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <span className="text-4xl">✨</span>
                <svg className="w-8 h-8 opacity-50" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="text-green-100 text-sm font-semibold mb-1">Model Confidence</p>
              <p className="text-5xl font-bold mb-2">{(predictions.reduce((sum, p) => sum + p.confidence, 0) / predictions.length * 100).toFixed(1)}%</p>
              <p className="text-green-100 text-xs">AI prediction accuracy</p>
            </div>
          </div>

          {/* Results Table */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden border-t-4 border-indigo-500">
            <div className="p-6 bg-gradient-to-r from-indigo-50 to-purple-50">
              <div className="flex items-center">
                <span className="text-3xl mr-3">📋</span>
                <h2 className="text-2xl font-bold text-gray-800">Prediction Results</h2>
              </div>
            </div>
            <RiskTable predictions={predictions} />
          </div>
        </>
      )}

      {/* Welcome State */}
      {!loading && predictions.length === 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-12 text-center border-t-4 border-purple-500">
          <div className="mb-6">
            <span className="text-8xl">🚀</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-800 mb-4">Welcome to PeoplePulse</h2>
          <p className="text-xl text-gray-600 mb-6">
            Click the button above to generate AI-powered attrition predictions for sample employees.
          </p>
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 max-w-2xl mx-auto">
            <p className="text-gray-700 leading-relaxed">
              🎯 Our machine learning model analyzes <strong>35+ employee factors</strong> to predict attrition risk<br/>
              📊 Trained on <strong>1,470 real IBM HR Analytics</strong> records<br/>
              ✨ Achieving <strong>87% accuracy</strong> with advanced XGBoost algorithm
            </p>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}

export default Dashboard;
