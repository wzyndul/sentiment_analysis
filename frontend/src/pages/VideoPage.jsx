import { useLocation } from "react-router-dom";
import { styled } from "@mui/system";
import { Box, Card, CardContent, Typography, Link } from "@mui/material";
import Stats from "../components/Stats/Stats";

const CenterBox = styled(Box)({
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  minHeight: "100vh",
});

const CardBox = styled(Box)({
  width: "50%",
});

const CenterText = styled(CardContent)({
  textAlign: "center",
});

const VideoPage = () => {
  const location = useLocation();
  const video = location.state.video;
  console.log(video);
  let stats = {
    negative: video.negative,
    num_comments: video.num_comments,
    positive: video.positive,
    rating: video.rating,
  };

  return (
    <CenterBox>
      <CardBox>
        <Card>
          <CenterText>
            <Typography variant="h5" gutterBottom>
              Sentiment Analysis Results
            </Typography>
            <Typography>
              <Link href={video.url} target="_blank" rel="noopener noreferrer">
                {video.url}
              </Link>
            </Typography>
            <Stats stats={stats} plot={video.plot} />
          </CenterText>
        </Card>
      </CardBox>
    </CenterBox>
  );
};

export default VideoPage;
