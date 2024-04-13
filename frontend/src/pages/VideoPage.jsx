import { useLocation } from "react-router-dom";
import { Box, styled } from "@mui/system";
import Stats from "../components/Stats/Stats";

const CenterBox = styled(Box)(({ theme }) => ({
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
  }));



const VideoPage = (props) => {
  const location = useLocation();
  const video = location.state.video;
  let stats = {
    negative: video.negative,
    num_comments: video.num_comments,
    positive: video.positive,
    rating: video.rating
  };

  return (
    <CenterBox>
      <Stats stats={stats} plot={video.plot} />
    </CenterBox>
  );
};

export default VideoPage;