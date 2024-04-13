import axios from "axios";
import React, { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import Filter from "../components/Search/Filter";
import ErrorDialog from "../components/Error/ErrorDialog";
import {
  Typography,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Box,
  Button,
} from "@mui/material";
import { styled } from "@mui/system";

const ChannelPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const creator = location.state.creator;
  const { channel_id } = useParams();
  const [videos, setVideos] = useState([]);
  const [displayedVideos, setDisplayedVideos] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [plotData, setPlotData] = useState([]);
  const [isHovered, setIsHovered] = useState(false);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);

  const TruncatedTitle = styled(Typography)({
    display: "-webkit-box",
    WebkitLineClamp: 2,
    WebkitBoxOrient: "vertical",
    overflow: "hidden",
    textOverflow: "ellipsis",
  });

  const StyledChannelName = styled(Typography)({
    textAlign: "center",
    backgroundColor: "#3f51b5",
    color: "#fff",
    fontFamily: "Arial",
    padding: "8px",
    borderRadius: "4px",
    marginBottom: "16px",
  });

  const SmallCardMedia = styled(CardMedia)({
    height: 120,
    width: 120,
  });

  const StyledBox = styled(Box)({
    backgroundColor: "#282c34",
    minHeight: "100vh",
  });

  const StyledCard = styled(Card)({
    boxShadow: "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
    borderRadius: "5px",
    margin: "10px",
    height: "120px",
  });

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setOpen(true);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `${
            import.meta.env.VITE_API_URL
          }videos/?channel_id=${channel_id}&search=${search}`
        );
        setVideos(response.data);
      } catch (error) {
        handleError("Error fetching data");
      }
    };

    fetchData();
  }, [channel_id, search]);

  useEffect(() => {
    const fetchPlotData = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}plot/?creator_id=${channel_id}`
        );
        setPlotData(response.data.plot);
      } catch (error) {
        handleError("Error fetching data");
      }
    };

    fetchPlotData();
  }, [channel_id]);

  useEffect(() => {
    setDisplayedVideos(videos.slice((page - 1) * 16, page * 16));
  }, [videos, page]);

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
        totalItems={videos.length}
      />
      <StyledChannelName
        variant="h4"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {creator.channel_name}
      </StyledChannelName>
      {isHovered && (
        <img
          src={`data:image/png;base64,${plotData}`}
          alt="sentiment over time plot"
          style={{
            width: "640px",
            height: "480px",
            display: "block",
            marginLeft: "auto",
            marginRight: "auto",
          }}
        />
      )}
      <Typography variant="subtitle1">{creator.url}</Typography>
      <Grid container spacing={2}>
        {displayedVideos.map((video) => (
          <Grid item xs={3} key={video.id}>
            <StyledCard>
              <Grid container>
                <Grid item xs={4}>
                  <a href={video.url}>
                    <SmallCardMedia
                      component="img"
                      image={video.image_url}
                      alt={video.title}
                    />
                  </a>
                </Grid>
                <Grid item xs={8}>
                  <CardContent>
                    <Box style={{ height: "3em", overflow: "hidden" }}>
                      <TruncatedTitle variant="body1" gutterBottom>
                        {video.title}
                      </TruncatedTitle>
                    </Box>
                    <Box style={{ height: "1em" }}>
                      <Typography variant="caption">
                        Published on: {video.time_published} <br />
                      </Typography>
                      <Button
                        variant="contained"
                        color="primary"
                        onClick={() =>
                          navigate(`/video/${video.video_id}`, {
                            state: { video },
                          })
                        }
                      >
                        View Video Details
                      </Button>
                    </Box>
                  </CardContent>
                </Grid>
              </Grid>
            </StyledCard>
          </Grid>
        ))}
      </Grid>
      {videos.length === 0 && <Typography>No videos found.</Typography>}
    </StyledBox>
  );
};

export default ChannelPage;
