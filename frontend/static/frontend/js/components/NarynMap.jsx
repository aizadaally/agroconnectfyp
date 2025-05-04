// frontend/static/frontend/js/components/NarynMap.jsx
const NarynMap = () => {
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    
    // Naryn districts
    const districts = [
      { id: 'at_bashy', name: 'At-Bashy', path: 'M10,120 L50,100 L90,110 L120,130 L110,170 L70,180 L20,160 Z', center: [65, 140] },
      { id: 'naryn', name: 'Naryn', path: 'M120,130 L150,120 L190,130 L200,170 L160,190 L110,170 Z', center: [155, 155] },
      { id: 'ak_talaa', name: 'Ak-Talaa', path: 'M150,120 L180,90 L220,100 L240,140 L200,170 L190,130 Z', center: [195, 125] },
      { id: 'jumgal', name: 'Jumgal', path: 'M200,170 L240,140 L280,150 L290,190 L250,210 L210,190 Z', center: [245, 175] },
      { id: 'kochkor', name: 'Kochkor', path: 'M180,90 L220,70 L270,80 L280,110 L240,140 L220,100 Z', center: [230, 100] },
    ];
  
    return (
      <div className="naryn-map-container">
        <h4 className="text-center mb-3">Naryn Region</h4>
        <svg viewBox="0 0 300 250" className="naryn-map">
          {districts.map(district => (
            <g key={district.id} onClick={() => setSelectedDistrict(district.id)}>
              <path
                d={district.path}
                className={`district-path ${selectedDistrict === district.id ? 'active' : ''}`}
              />
              <text x={district.center[0]} y={district.center[1]} className="district-label">
                {district.name}
              </text>
            </g>
          ))}
        </svg>
        
        <div className="district-selector">
          <select 
            className="form-select" 
            value={selectedDistrict || ''} 
            onChange={(e) => setSelectedDistrict(e.target.value)}
          >
            <option value="">Select District</option>
            {districts.map(district => (
              <option key={district.id} value={district.id}>
                {district.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    );
  }