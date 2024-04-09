import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; 
import Filter from '../components/Search/Filter';

const ChannelPage = () => {
  const { channel_id } = useParams();
  const [videos, setVideos] = useState([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);

  const fetchData = async () => {
    const response = await fetch(
        `${import.meta.env.VITE_API_URL}videos/?channel_id=${channel_id}&search=${search}`
      );
      const data = await response.json();
      console.log(`${import.meta.env.VITE_API_URL}videos/?channel_id=${channel_id}&search=${search}`);
      console.log(data);
    setVideos(data);
  };


  useEffect(() => {
    fetchData();
  }, [search, page]);

  const handleSearch = event => {
    event.preventDefault();
    setSearch(event.target.elements.search.value);
  };

  const handlePageChange = newPage => {
    setPage(newPage);
  };

  return (
    <div>
      <Filter onSearch={handleSearch} />
      {videos.map(video => (
        <div key={video.id}>
          <a href={video.url}>
            <img src={video.imageUrl} alt={video.title} />
          </a>
          <h2>{video.title}</h2>
          <p>Published on: {video.timePublished}</p>
        </div>
      ))}
      <div>
        {page > 1 && <button onClick={() => handlePageChange(page - 1)}>Previous</button>}
        <span>Page {page}</span>
        {videos.length > 0 && <button onClick={() => handlePageChange(page + 1)}>Next</button>}
      </div>
    </div>
  );
};

export default ChannelPage;