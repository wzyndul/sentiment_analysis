import * as React from 'react';
import { styled } from '@mui/system';
import { Box, Card, CardContent, Button, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const CenterBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
}));

const CardBox = styled(Box)(({ theme }) => ({
  width: '50%',
}));

const CenterText = styled(Box)(({ theme }) => ({
  textAlign: 'center',
}));

export default function MainPage() {
  const navigate = useNavigate();
  const [youtubeUrl, setYoutubeUrl] = React.useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    const response = await fetch(`${import.meta.env.VITE_API_URL}analysis/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ youtube_url: youtubeUrl }),
    });

    const data = await response.json();


    navigate('/video-analysis', { state: { data: data, url: youtubeUrl } });
  };


  return (
    <CenterBox>
      <CardBox>
        <Card>
          <CardContent>
            <CenterText>
              <Typography variant="h5" gutterBottom>
                YouTube Comments
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Enter a YouTube video link to analyze comments.
              </Typography>
              <Box component="form" onSubmit={handleSubmit} mt={2}>
                <TextField
                  fullWidth
                  id="youtube_url"
                  label="YouTube Video URL"
                  placeholder="Enter YouTube Video URL"
                  margin="normal"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                />
                <Button variant="contained" type="submit">
                  Analyze
                </Button>
              </Box>
            </CenterText>
          </CardContent>
        </Card>
      </CardBox>
    </CenterBox>
  );
};