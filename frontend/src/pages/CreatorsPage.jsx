import React, { useState, useEffect } from 'react';
import { Box, Card, CardContent, CardMedia, Typography, TextField, Button, Pagination} from '@mui/material';
import { styled } from '@mui/system';
import { Link } from 'react-router-dom';

function Creators() {

const SmallCardMedia = styled(CardMedia)(({ theme }) => ({
    height: 50,
    width: 50,
  }));

  const [creators, setCreators] = useState([]);
  const [displayedCreators, setDisplayedCreators] = useState([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchCreators = async () => {
      const response = await fetch(`${import.meta.env.VITE_API_URL}creators/?search=${search}`);
      const data = await response.json();
      setCreators(data);
    };

    fetchCreators();
  }, [search]);

  useEffect(() => {
    setDisplayedCreators(creators.slice((page - 10) * 10, page * 10));
  }, [creators, page]);

  return (
    <Box>
      <form>
        <TextField label="Search creators" value={search} onChange={e => setSearch(e.target.value)} />
      </form>
      {displayedCreators.map(creator => (
        <Card key={creator.channel_id}>
          <SmallCardMedia component="img" image={creator.picture_url} alt={creator.channel_name}/>
          <CardContent>
            <Typography>{creator.channel_name}</Typography>
            <Button component={Link} to={`/channel_view/${creator.channel_id}`}>View Profile</Button>
          </CardContent>
        </Card>
      ))}
      {creators.length === 0 && <Typography>No creators found.</Typography>}
      <Pagination count={Math.ceil(creators.length / 10)} page={page} onChange={(_, value) => setPage(value)} />
    </Box>
  );
}

export default Creators;