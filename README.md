# hass-media-player-poster
Display images from google image search for the media played in hass media player.

The script loads the first image from google images that is maching the file name. 

95% of my test it was able to provide the exact poster image.<br />
4% it was relevant image from the movie but not the poster.<br />
1% unrelated image.<br />

![example](Screenshot_hass_mpc.png)


To make this work you'll have to:

1. Configure dl.py by updating these lines:

	<pre>
	# Path where the image will be saved - your hass file camera shuold point here
	save_path = '/ram'
	
	# Name for the downloaded image - your hass file camera shuold look for this file
	file_name = 'movie_data'
	
	# Password for your hass instance - this is needed to get the filename from the mediaplayer component.
	hass_password = 'your_hass_password'
	
	# This is the name of the media player we'll track and provide images/posters
	mpc_name = 'mpclivingroom'
	</pre>
  
2. Make a file camera in home-assistant that uses the image from save_path + file_name
3. Create a shell command in home assitant like the one below:

 <pre>shell_command:   
    get_movie_img: 'sudo python3 /path/to/script/dl.py'</pre>

(my save location requeres root that is why I am calling the script with sudo)

4. Create an automation in home-assistant that will call the script once the player state is changed:

 <pre> - id: e
    alias: Movie Poster
    trigger:
    - platform: state
      entity_id: media_player.mpclivingroom

    action:  
    - service: shell_command.get_movie_img </pre>
  
  
You shuold be all set now.  
