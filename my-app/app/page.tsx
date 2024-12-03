"use client";
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ManualInput from '@/pages/ManualInput';
import LampDemo from '@/pages/new_page'

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/r" element={<LampDemo />} />
                <Route path="/" element={<ManualInput />} />
            </Routes>
        </Router>
    );
};

export default App;
