import { Box, Typography } from '@mui/material';

function Stats({ stats, plot }) {
  return (
    <Box>
      <Typography align="center">Positive: {stats.positive}</Typography>
      <Typography align="center">Negative: {stats.negative}</Typography>
      <Typography align="center">Number of comments: {stats.num_comments}</Typography>
      <Typography align="center">Rating: {stats.rating}</Typography>
      <Box display="flex" justifyContent="center">
        <img
          src={`data:image/png;base64,${plot}`}
          alt="sentiment over time plot"
          style={{ width: '640px', height: '480px' }}
        />
      </Box>
    </Box>
  );
}

export default Stats;