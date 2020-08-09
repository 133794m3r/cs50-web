# Project 2 Flack
This is the project to make a basic web chat thing.

## Youtube Demo
(Youtube Demo)[https://www.youtube.com/watch?v=PtXNmDIl2lQ]

## Details
All of the items are laid out into sections.


### Features
- Private Messages(between users)
    - Also shows unread messages via a pill icon beside them.
- Private Channels(with a password)
    - private channels can have repeated names(as the actual name is based upon their uuid and the channel name)
- Adding Channels
    - If user exists it tells them such.
- Joining a private channel
    - If the password is incorrect modal tells them as much.
- choosing a display name
    - if their name already exists a modal tells them to chose another.
- remembering the user after returning(including private channels/pms)
    - Rejoining causes them to get all of the channels they've already authenticated too, and also all of the global channels.
- Having users click a link to join a channel.
    - This also includes private channels. If it is a private channel the password will be included as part of the change channel link.
    
### Each Files features
Each one is based upon their file and they are sorted based upon folder.
### static folder
This holds the javascript and CSS files.
#### js
#### boostrap.js  
This is the boostrap javascript file for modals and the like.
#### script.js
This file contains all of the socket creation and all of the other utility files.
#### css
These are the css files.
#### boostrap.css
Basic boostrap stuff.
#### style.css
The css style sheets for my custon styling information.

#### templates
These are my template files.
#### index.html
This is the primary page. I decided to just make it a single file.
#### layout.html
The base file that I was going to use for multiple pages but I decided to just keep it as a single page item.
#### index-design.html
This is just my mockup of the index page with the design elements as I was thinking of them.

### application.py
This contains the routes and all of the related python code for the entire application.

### requirements.txt
This is the pip requirements file so that you can also get it up and going after cloning/downloading the files.
