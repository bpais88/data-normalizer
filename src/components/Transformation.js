import React, { useState } from 'react';
import axios from 'axios';

function Transformation() {
    const [source, setSource] = useState({});
    const [targetSchema, setTargetSchema] = useState([]);
    const [mappings, setMappings] = useState({});
    const [transformations, setTransformations] = useState({});

    const handleTransform = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/transform', {
                source,
                target_schema: targetSchema,
                mappings,
                transformations,
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error transforming data:', error);
        }
    };

    return (
        <div>
            {/* Add UI elements to capture source, targetSchema, mappings, and transformations */}
            <button onClick={handleTransform}>Transform</button>
        </div>
    );
}

export default Transformation;
