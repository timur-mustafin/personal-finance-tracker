
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ImportExport from './pages/ImportExport';
import Login from './pages/Login';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('access') || localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
};

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
  <Route path="/import-export" element={<PrivateRoute><ImportExport /></PrivateRoute>} />
</Routes>
    </BrowserRouter>
  );
}
