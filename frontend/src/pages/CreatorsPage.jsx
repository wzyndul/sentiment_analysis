import axios from "axios";
import React, { useState, useEffect } from "react";
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Grid,
} from "@mui/material";
import { styled } from "@mui/system";
import Filter from "../components/Search/Filter";
import ErrorDialog from "../components/Error/ErrorDialog";
import { useNavigate } from "react-router-dom";

function Creators() {
  const navigate = useNavigate();
  const [creators, setCreators] = useState([]);
  const [displayedCreators, setDisplayedCreators] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);

  const RoundCardMedia = styled(CardMedia)({
    height: 50,
    width: 50,
    borderRadius: "50%",
  });

  const StyledBox = styled(Box)({
    flexGrow: 1,
    margin: "16px",
    minHeight: "100vh",
  });

  const StyledGridItem = styled(Grid)({
    height: "200px",
    width: "200px",
  });

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setOpen(true);
  };

  useEffect(() => {
    const fetchCreators = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}creators/?search=${search}`
        );
        setCreators(response.data);
      } catch (error) {
        handleError("Error fetching creators");
      }
    };

    fetchCreators();
  }, [search]);

  useEffect(() => {
    setDisplayedCreators(creators.slice((page - 1) * 16, page * 16));
  }, [creators, page]);

  return (
    <StyledBox>
      <ErrorDialog
        open={open}
        handleClose={() => setOpen(false)}
        error={error}
      />
      <Filter
        search={search}
        setSearch={setSearch}
        page={page}
        setPage={setPage}
        totalItems={creators.length}
      />
      <Grid container spacing={2}>
        {displayedCreators.map((creator) => (
          <StyledGridItem item xs={3} key={creator.channel_id}>
            <Card>
              <RoundCardMedia
                component="img"
                image={creator.picture_url}
                alt={creator.channel_name}
              />
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {creator.channel_name}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() =>
                    navigate(`/channel/${creator.channel_id}`, {
                      state: { creator },
                    })
                  }
                >
                  View Profile
                </Button>
              </CardContent>
            </Card>
          </StyledGridItem>
        ))}
      </Grid>
      {creators.length === 0 && <Typography>No creators found.</Typography>}
    </StyledBox>
  );
}

export default Creators;
