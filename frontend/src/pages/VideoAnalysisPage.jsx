import { styled } from '@mui/system';
import { Box, Card, CardContent, Typography, Link } from '@mui/material';
import { useLocation } from 'react-router-dom';
import Stats from '../components/Stats/Stats';

const CenterBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
}));

const CardBox = styled(Box)(({ theme }) => ({
  width: '50%',
}));

const CenterText = styled(CardContent)(({ theme }) => ({
  textAlign: 'center'
}));

function VideoAnalysis() {
  const location = useLocation();
  const { data, url } = location.state;
  return (
    <CenterBox>
      <CardBox>
        <Card>
          <CenterText>
            <Typography variant="h5" gutterBottom>
              Sentiment Analysis Results
            </Typography>
            <Typography>
              <Link href={url} target="_blank" rel="noopener noreferrer">{url}</Link>
            </Typography>
            <Stats stats={data.stats} plot={data.plot} />
          </CenterText>
        </Card>
      </CardBox>
    </CenterBox>
  );
}

export default VideoAnalysis;