<h1 align="center" id="title">Sentiment Analysis App</h1>

<p id="description">This project uses the combined capabilities of Django, React, and a sentiment analysis model based on Recurrent Neural Networks (RNNs).
  
By integrating with the YouTube API, users can input a video URL, which triggers the backend (made in Django) to scrape comments. These comments are then analyzed using the RNN-based sentiment analysis model.

Frontend, developed with React, facilitates user interaction and presents the sentiment analysis results in an intuitive interface. This comprehensive solution offers users a seamless experience for extracting insights from YouTube video comments through sentiment analysis</p>   



<p> Main Page: user can  paste URL to the YouTube video to analyse it</p>
<img src=".\img\main.png" alt="Main Page" width="100%">

<p>Results Page: results of the analysis</p>

<img src=".\img\plot.png" alt="Plot" width="100%">

<p> Creators Page: user can filter creators and enter their profiles</p>

<img src=".\img\creators.png" alt="Creators Page" width="100%">

<p> Videos Page: user can filter videos, watch them after clicking thumbnail picture and enter video for analysis results</p>

<img src=".\img\videos.png" alt="Videos Page" width="100%">

<p> Videos Page: statistics for all creators videos are displayed when user holds mouse cursor at channel name</p>

<img src=".\img\creator_plot.png" alt="Creator Plot" width="100%">



<h2>🧐 Features</h2>

Here're some of the project's best features:

* Fetching YouTube comments from a user-provided URL using YouTube's API
* Performing sentiment analysis on the fetched comments
* Displaying the sentiment analysis results in a user-friendly interface
* Creating visual plots based on the sentiment analysis results
* Backend server built with Python, responsible for data processing and sentiment analysis
* Frontend client developed using JavaScript and React, communicating with the backend through an API
* Utilization of npm and pip for managing dependencies
* Seamless integration between the frontend and backend for a robust and efficient application performance

<h2>💻 Built with</h2>

Technologies used in the project:

* Python
* Django
* pip
* YouTube Data API v3
* Material UI
* Axios
* JavaScript
* Axios
* npm

<h2>🛠️ Installation Steps</h2>

To get started with this project, clone the repository and install the dependencies:

Frontend:
```
npm install
```
Backend:
```
pip install -r "requirements.txt"
```

Then start the development server:

Frontend:
```
npm run dev
```
Backend:
```
python manage.py runserver
```

Also in .env file you have to provide YOUTUBE_API_KEY and VITE_API_URL
