import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ShapChart from '../components/ShapChart';
import { predictEmployee, simulateIntervention } from '../api';

function EmployeeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Sample employee data - in production, fetch from API
  const sampleEmployee = {
    employee_id: id,
    age: 35,
    gender: "Male",
    department: "Sales",
    job_role: "Sales Executive",
    education: 3,
    education_field: "Life Sciences",
    years_at_company: 5,
    years_in_current_role: 2,
    years_since_last_promotion: 3,
    years_with_curr_manager: 2,
    num_companies_worked: 2,
    monthly_income: 5000.0,
    percent_salary_hike: 12,
    stock_option_level: 1,
    training_times_last_year: 2,
    job_satisfaction: 3,
    work_life_balance: 2,
    environment_satisfaction: 3,
    relationship_satisfaction: 3,
    performance_rating: 3,
    business_travel: "Travel_Frequently",
    distance_from_home: 10,
    marital_status: "Single",
    overtime: "Yes"
  };

  useEffect(() => {
    loadPrediction();
  }, [id]);

  const loadPrediction = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await predictEmployee(sampleEmployee);
      setPrediction(result);
    } catch (err) {
      setError('Failed to load prediction');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Loading employee details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">{error}</div>
        <button className="btn" onClick={() => navigate('/')}>
          Back to Dashboard
        </button>
      </div>
    );
  }

  if (!prediction) {
    return null;
  }

  return (
    <div className="container">
      <button 
        className="btn" 
        onClick={() => navigate('/')}
        style={{ marginBottom: '1.5rem' }}
      >
        ← Back to Dashboard
      </button>

      <div className="risk-table-container" style={{ marginBottom: '2rem' }}>
        <h2>Employee: {prediction.employee_id}</h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1.5rem' }}>
          <div>
            <p style={{ color: '#7f8c8d', fontSize: '0.9rem' }}>Attrition Risk</p>
            <p className={`kpi-value ${prediction.risk_level.toLowerCase()}`}>
              {(prediction.attrition_probability * 100).toFixed(1)}%
            </p>
          </div>
          <div>
            <p style={{ color: '#7f8c8d', fontSize: '0.9rem' }}>Risk Level</p>
            <span className={`risk-badge ${prediction.risk_level.toLowerCase()}`} style={{ fontSize: '1rem', padding: '0.5rem 1rem' }}>
              {prediction.risk_level}
            </span>
          </div>
          <div>
            <p style={{ color: '#7f8c8d', fontSize: '0.9rem' }}>Model Confidence</p>
            <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
              {(prediction.confidence * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
          <h4 style={{ marginBottom: '0.5rem' }}>Recommendation</h4>
          <p>{prediction.recommendation}</p>
        </div>
      </div>

      <ShapChart shapValues={prediction.top_factors} />

      <div className="chart-container">
        <h3>Top Risk Factors</h3>
        <table className="risk-table">
          <thead>
            <tr>
              <th>Feature</th>
              <th>Current Value</th>
              <th>Impact on Risk</th>
              <th>Direction</th>
            </tr>
          </thead>
          <tbody>
            {prediction.top_factors.map((factor, idx) => (
              <tr key={idx}>
                <td><strong>{factor.feature}</strong></td>
                <td>{typeof factor.value === 'number' ? factor.value.toFixed(2) : factor.value}</td>
                <td>{Math.abs(factor.impact).toFixed(4)}</td>
                <td>
                  {factor.impact > 0 ? (
                    <span style={{ color: '#e74c3c' }}>↑ Increases Risk</span>
                  ) : (
                    <span style={{ color: '#27ae60' }}>↓ Decreases Risk</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="chart-container">
        <h3>Recommended Actions</h3>
        <ul style={{ lineHeight: '1.8', paddingLeft: '1.5rem' }}>
          <li>Schedule a retention conversation with the employee's manager</li>
          <li>Review compensation and benefits package</li>
          <li>Discuss career development and growth opportunities</li>
          <li>Evaluate work-life balance and overtime concerns</li>
          <li>Consider flexible work arrangements if applicable</li>
          <li>Provide additional training and development resources</li>
        </ul>
      </div>
    </div>
  );
}

export default EmployeeDetail;
