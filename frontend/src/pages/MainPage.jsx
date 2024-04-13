import axios from "axios";
import React, { useState } from "react";
import { styled } from "@mui/system";
import {
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import ErrorDialog from "../components/Error/ErrorDialog";

const CenterBox = styled(Box)(({ theme }) => ({
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  minHeight: "100vh",
}));

const CardBox = styled(Box)(({ theme }) => ({
  width: "50%",
}));

const CenterText = styled(Box)(({ theme }) => ({
  textAlign: "center",
}));

export default function MainPage() {
  const navigate = useNavigate();
  const [youtubeUrl, setYoutubeUrl] = React.useState("");
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setOpen(true);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}analysis/`,
        { youtube_url: youtubeUrl },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = response.data;
      navigate("/video-analysis", { state: { data: data, url: youtubeUrl } });
    } catch (error) {
      handleError(
        "Error occurred while analyzing video, check the URL or try again later."
      );
    }
  };

  return (
    <CenterBox>
      <CardBox>
        <Card>
          <ErrorDialog
            open={open}
            handleClose={() => setOpen(false)}
            error={error}
          />
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
}
