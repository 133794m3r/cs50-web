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
- User control panel(simply lets them update their password right now)


### Requirements.txt
This includes all packages required.