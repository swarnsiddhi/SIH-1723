"use client";
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ManualInput from '@/pages/ManualInput';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<ManualInput />} />
            </Routes>
        </Router>
    );
};

export default App;
