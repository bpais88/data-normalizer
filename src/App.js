import React from 'react';
import FileUpload from './components/FileUpload';
import Transformation from './components/Transformation';

function App() {
    return (
        <div className="App">
            <h1>Data Normalizer</h1>
            <FileUpload />
            <Transformation />
        </div>
    );
}

export default App;