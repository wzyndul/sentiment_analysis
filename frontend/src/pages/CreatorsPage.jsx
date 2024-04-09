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
import { Link } from "react-router-dom";
import Filter from "../components/Search/Filter";

function Creators() {

  const SmallCardMedia = styled(CardMedia)(({ theme }) => ({
    height: 50,
    width: 50,
    borderRadius: "50%",
  }));

  const StyledBox = styled(Box)({
    flexGrow: 1,
    margin: '16px',
  });

  const [creators, setCreators] = useState([]);
  const [displayedCreators, setDisplayedCreators] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchCreators = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}creators/?search=${search}`
      );
      const data = await response.json();
      setCreators(data);
    };

    fetchCreators();
  }, [search]);

  useEffect(() => {
    setDisplayedCreators(creators.slice((page - 1) * 16, page * 16));
  }, [creators, page]);

  return (
    <StyledBox>
      <Filter
        search={search}
        setSearch={setSearch}
        page={page}
        setPage={setPage}
        totalItems={creators.length}
      />
      <Grid container spacing={2}>
        {displayedCreators.map((creator) => (
          <Grid item xs={3} key={creator.channel_id}>
            <Card>
              <SmallCardMedia
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
                  component={Link}
                  to={{
                    pathname: `/channel/${creator.channel_id}`
                  }}
                >
                  View Profile
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      {creators.length === 0 && <Typography>No creators found.</Typography>}
    </StyledBox>
  );
}

export default Creators;
