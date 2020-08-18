# music_scout

This is an app I wrote to web scrape the music played by certain select radio station programs or listed on sites like Pitchfork and 
create Spotify playlists based for those tracks.

To be able to run this, you'll need all the library dependencies and also the following:

1. A folder called 'databases' that shares a parent with your working directory (i.e. it is located at '/../databases/'
2. Store your Spotify login credentials in a file here: '../showtime_creds/config.yaml' as follows:  
      username: 'loremipsum_username'
      client_id: 'loremipsum_client_id'
      client_secret: 'loremipsum_client_secrete'
      redirect_uri: 'https://localhost:8080'

Then run main.py and select the shows you want to make playlists for!
