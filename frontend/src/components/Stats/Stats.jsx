import { Box, Typography } from '@mui/material';

function Stats({ stats, plot }) {
  return (
    <Box>
      <Typography>Positive: {stats.positive}</Typography>
      <Typography>Negative: {stats.negative}</Typography>
      <Typography>Number of comments: {stats.num_comments}</Typography>
      <Typography>Rating: {stats.rating}</Typography>
      <img
        src={`data:image/png;base64,${plot}`}
        alt="sentiment over time plot"
        style={{ width: '640px', height: '480px' }}
      />
    </Box>
  );
}

export default Stats;