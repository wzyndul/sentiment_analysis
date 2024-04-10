import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Main from './pages/MainPage';
import Creators from './pages/CreatorsPage';
import Channel from './pages/ChannelPage';
import Video from './pages/VideoPage';
import VideoAnalysis from './pages/VideoAnalysisPage';
import Navbar from './components/Header/Navbar';
import './App.css';

function App() {
  return (
    <div className='app'>
      <Router>
        <Navbar/>
        <Routes>
          <Route path="/" element={<Main/>}/>
          <Route path="/creators" element={<Creators/>}/>
          <Route path="/channel/:channel_id" element={<Channel/>}/>
          <Route path="/video/:video_id" element={<Video/>}/>
          <Route path="/video-analysis" element={<VideoAnalysis/>}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;