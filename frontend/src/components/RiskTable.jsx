import { useNavigate } from 'react-router-dom';

function RiskTable({ predictions }) {
  const navigate = useNavigate();

  const handleRowClick = (employeeId) => {
    navigate(`/employee/${employeeId}`);
  };

  if (!predictions || predictions.length === 0) {
    return (
      <div className="risk-table-container">
        <h2>High Risk Employees</h2>
        <p>No predictions available. Please add employee data and generate predictions.</p>
      </div>
    );
  }

  // Sort by risk probability descending
  const sortedPredictions = [...predictions].sort(
    (a, b) => b.attrition_probability - a.attrition_probability
  );

  return (
    <div className="risk-table-container">
      <h2>Employee Attrition Risk Overview</h2>
      <table className="risk-table">
        <thead>
          <tr>
            <th>Employee ID</th>
            <th>Risk Level</th>
            <th>Probability</th>
            <th>Confidence</th>
            <th>Top Factor</th>
            <th>Recommendation</th>
          </tr>
        </thead>
        <tbody>
          {sortedPredictions.map((pred) => (
            <tr 
              key={pred.employee_id} 
              onClick={() => handleRowClick(pred.employee_id)}
            >
              <td><strong>{pred.employee_id}</strong></td>
              <td>
                <span className={`risk-badge ${pred.risk_level.toLowerCase()}`}>
                  {pred.risk_level}
                </span>
              </td>
              <td>{(pred.attrition_probability * 100).toFixed(1)}%</td>
              <td>{(pred.confidence * 100).toFixed(1)}%</td>
              <td>
                {pred.top_factors && pred.top_factors.length > 0 
                  ? pred.top_factors[0].feature 
                  : 'N/A'}
              </td>
              <td style={{ fontSize: '0.85rem', maxWidth: '300px' }}>
                {pred.recommendation || 'No recommendation'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default RiskTable;
