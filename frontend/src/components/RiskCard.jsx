function RiskCard({ title, value, trend, riskLevel }) {
  const getRiskClass = () => {
    if (riskLevel === 'high') return 'high';
    if (riskLevel === 'medium') return 'medium';
    return 'low';
  };

  return (
    <div className="kpi-card">
      <h3>{title}</h3>
      <div className={`kpi-value ${getRiskClass()}`}>
        {value}
      </div>
      {trend && <p style={{ fontSize: '0.85rem', color: '#7f8c8d' }}>{trend}</p>}
    </div>
  );
}

export default RiskCard;
