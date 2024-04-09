import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from './pages/MainPage';
import Creators from './pages/Creators';
import Channel from './pages/Channel';
import Video from './pages/Video';
import VideoAnalysis from './pages/VideoAnalysis';
import Navbar from './components/Header/Navbar';
import './App.css';

function App() {
  return (
    <div>
      <Router>
        <Navbar/>
        <Routes>
          <Route path="/" element={<MainPage/>}/>
          <Route path="/creators" element={<Creators/>}/>
          <Route path="/channel/:id" element={<Channel/>}/>
          <Route path="/video/:id" element={<Video/>}/>
          <Route path="/video-analysis/:id" element={<VideoAnalysis/>}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;