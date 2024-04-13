import { AppBar, Toolbar,Button } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

function Navbar() {
  return (
    <AppBar position="static" sx={{ backgroundColor: "#333" }}>
      <Toolbar>
        <Button color="inherit" component={RouterLink} to="/">
          Main Page
        </Button>
        <Button color="inherit" component={RouterLink} to="/creators">
          Creators
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
