import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

function ShapChart({ shapValues }) {
  if (!shapValues || shapValues.length === 0) {
    return <p>No SHAP values available</p>;
  }

  // Prepare data for chart
  const data = shapValues.map(item => ({
    feature: item.feature,
    impact: item.impact,
    value: item.value
  }));

  // Color based on impact direction
  const getColor = (impact) => {
    return impact > 0 ? '#e74c3c' : '#27ae60';
  };

  return (
    <div className="chart-container">
      <h3>Feature Impact Analysis (SHAP Values)</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 150, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="feature" type="category" />
          <Tooltip 
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                return (
                  <div style={{
                    backgroundColor: 'white',
                    padding: '10px',
                    border: '1px solid #ccc',
                    borderRadius: '4px'
                  }}>
                    <p><strong>{payload[0].payload.feature}</strong></p>
                    <p>Value: {payload[0].payload.value}</p>
                    <p>Impact: {payload[0].value.toFixed(4)}</p>
                    <p>{payload[0].value > 0 ? 'Increases' : 'Decreases'} attrition risk</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Legend />
          <Bar dataKey="impact" name="SHAP Impact">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.impact)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#7f8c8d' }}>
        <p><strong>Interpretation:</strong></p>
        <p>🔴 Red bars indicate factors that <strong>increase</strong> attrition risk</p>
        <p>🟢 Green bars indicate factors that <strong>decrease</strong> attrition risk</p>
      </div>
    </div>
  );
}

export default ShapChart;
