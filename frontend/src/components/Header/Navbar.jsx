import { styled } from '@mui/system';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const StyledAppBar = styled(AppBar)({
  backgroundColor: '#333',
});



function Navbar() {
  return (
    <StyledAppBar position="static">
      <Toolbar>
        <Button color="inherit" component={RouterLink} to="/">Main Page</Button>
        <Button color="inherit" component={RouterLink} to="/creators">Creators</Button>
      </Toolbar>
    </StyledAppBar>
  );
}

export default Navbar;