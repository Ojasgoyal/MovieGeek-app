# MovieGeek

MovieGeek is a personal movie database web application designed for users who want to explore movies, actors, and save their favorite movies in a personalized dashboard. The website integrates the **TMDB API** to fetch movie and person details, allowing users to search for movies and people, view detailed information, create user profiles, and browse other users' profiles. It is built using **Flask**, **SQLite3**, and other web technologies to provide a clean, interactive, and responsive user experience. This project was developed as part of the **CS50x** final project.

## Features

- **User Authentication**: Users can sign up, log in, and manage their profiles.
- **Movie Search**: Search for movies using the TMDB API.
- **People Search**: Search for actors, directors, and other movie industry professionals.
- **Movie and Person Details**: View detailed pages for movies and people, including cast, crew, ratings, and more.
- **Personal Dashboard**: Registered users can save movies to their profile, creating a personalized movie collection.
- **Browse Other Users' Profiles**: Users can search for and view the profiles of other users, exploring their saved movies and preferences.
- **Responsive Design**: The website is fully responsive, optimized for both mobile and desktop screens.

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3
  - Bootstrap 4
  - Google Fonts (Poppins)
  - JavaScript (for interactive features)

- **Backend**:
  - Python (Flask)
  - SQLite3 (Database)
  - TMDB API (for fetching movie and person data)

## Folder Structure

- **app.py**: Main Flask application file handling routing and logic.
- **models.py**: Contains functions to interact with the SQLite database.
- **moviegeek.db**: SQLite database file.
- **static/**: Contains static assets like CSS, JS, and images.
  - `styles.css`: Custom styles for the website.
  - `bgimage.webp`: Background image for the landing page.
- **templates/**: Contains HTML templates for rendering pages.
  - `layout.html`: Common layout template for header, footer, and shared elements.
  - `error.html`: Custom error page for 404 errors.
  - `index.html`: Landing page with login and Signup Buttons.
  - `login.html` and `signup.html`: Forms for user authentication.
  - `profile.html`: User profile page showing saved movies and profile details.
  - `search.html`: Displays search results for movies based on the user’s query.
  - `person.html`: Displays search results for people (actors, directors).
  - `movie.html` and `persondata.html`: Detailed pages for movies and people.
- **requirements.txt**: List of Python dependencies for the project.

## Project Overview

The core functionality of MovieGeek revolves around allowing users to:
- **Search for Movies and People**: Through separate search pages, users can look up movies and stars (actors, directors, etc.) from the vast collection available on the TMDB database.
- **Save Favorite Movies**: Registered users can save their favorite movies to their profile, creating a personalized movie collection.
- **View Detailed Pages**: Each movie and person has a detailed page that includes additional information like plot summaries, cast, crew, ratings, and more.
- **Manage Profile**: Users can create and manage their profiles to track and access their favorite movies.
- **Browse Other Users' Profiles**: Users can search for and view the profiles of other users, exploring their saved movies and gaining insight into their movie preferences.

## Design Choices

### Why Flask and SQLite3?
Flask was chosen for its simplicity and flexibility, which allowed for rapid development of the web app. It is perfect for small to medium-sized applications like this, where the use of a more complex framework like Django would be unnecessary. SQLite3 was selected as the database due to its lightweight nature and the fact that this project does not require a high-traffic solution.

### Why TMDB API?
The TMDB API provides access to an extensive and well-organized database of movies, TV shows, and people. It offers detailed metadata, including ratings, cast and crew details, images, and trailers, making it an ideal choice for the project's needs.

### User Interface Design
The design is minimalist and user-friendly, using Bootstrap for responsive design and custom CSS to enhance the user experience. The application is designed to be intuitive, with clear navigation between pages. The search functionality is prominently displayed, and detailed pages for movies and people present rich, well-organized information. The ability to view other users' profiles encourages social interaction and adds a community aspect to the app.

## Future Enhancements

While MovieGeek is fully functional, there are several potential features to implement:
- **Movie Reviews and Ratings**: Allow users to leave reviews or ratings for movies.
- **Recommendation System**: Build a recommendation engine that suggests movies based on user preferences.
- **Social Sharing**: Allow users to share their favorite movies on social media platforms.

## Conclusion

MovieGeek is a fun and interactive web application for movie lovers. It provides users with the ability to explore movies, save their favorites, and manage personal profiles. Built using Flask, SQLite3, and the TMDB API, the project showcases web development skills with a focus on user-friendly design and API integration. This project serves as a solid foundation for further development in web applications and external API usage.

## Acknowledgments

- [TMDB API](https://www.themoviedb.org/documentation/api) for providing movie data.
- The CS50x course for inspiration and guidance in building this project.
- Bootstrap for the responsive design framework.