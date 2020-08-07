#CTF Club/Capstone Project
This folder contains the Capstone project that I wrote. It has the features listed below and checks all of the boxes required.

## Required Features
- [x] Utilizes Django
- [x] Uses Multiple Models
- [x] Uses JavaScript on the Front-end
- [x] Uses Python on the backend.
- [x] Completely distinct from other projects from the courses.
- [x] Has multiple different views and templates.
- [x] Mobile Responsive(via BootStrap handling the majority of the theming.)

## Actual Feature List
- Custom Password Authentication Hasher Class(Uses Scrypt from hashlib instead of default django hashers)
- Users can Login/Logout.
- CSRF Protected
- Uses modern Fetch instead of XMLHTTPRequest
- Users can submit data to the server via fetch and get back results w/o a full page refresh.
- Templates are generated programmatically
- There is an admin page that requires specific authentication to ge to it.
- Uses extra modules that are called from the view.
- Mobile Responsive
- From the Admin page someone can modify/create a challenge by simply typing in some information into the modal dialogue and letting the server do the rest.
- Views that should only be seen by logged in users are proteced via decorators,
    - only certain methods are allowed for each view.
- Models are setup with many different relational types.
- Challenges are shown via a modal-dialogue for the user upon clicking on one.
- User control panel(simply lets them update their password right now, and shows their solves)
- Can modify the hints of any challenge and have the data reflected on the page as long as the response is OK.
- Can add hints to a challenge after creation and it'll add them to their local view.
- Admin can see the number of solves for any challenge.
- Updating a challenge causes all solves to be nullified and removed from the solves for the user.
- Uses ZXCVBN for the password strength, along with giving them feedback for their passwords.
- Attempting a solve will result in an alert showing. If it's successful then they'll get the "solved" message. If they didn't then it'll show "wrong answer." Also the alert will dissappear after some period of time.
- The modal dialogues for the admin view or the challenge view can all be stacked upon eachother while not causing the other views to be obscured.


### Requirements
Also requires Python 3.6 or later as it utilizes hashlib for Scrypt.

pip3 install -r requirements.txt
This includes all packages required.
