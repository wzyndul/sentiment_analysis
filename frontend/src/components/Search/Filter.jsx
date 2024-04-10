import React from 'react';
import { TextField, Pagination, Box, Paper, styled } from '@mui/material';

const StyledPaper = styled(Paper)({
  padding: '16px',
  marginBottom: '16px',
});



const StyledBox = styled(Box)({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
});

function Filter({ search, setSearch, page, setPage, totalItems }) {
  return (
    <StyledPaper elevation={3}>
      <StyledBox>
        <TextField 
          label="Search" 
          value={search} 
          onChange={e => setSearch(e.target.value)} 
          variant="outlined"
          size="small"
        />
        <Pagination 
          count={Math.ceil(totalItems / 16)} 
          page={page} 
          onChange={(_, value) => setPage(value)} 
          color="primary"
        />
      </StyledBox>
    </StyledPaper>
  );
}

export default Filter;