# CS50W Portfolio Assignments

## 2018 Folder
This folder contains all of the assignments for the 2018 version of the course that I completed.

## Sampler
Basic page using some bootstrap component.

Features(as per the requirements)
-Your website must contain at least four different .html pages, and it should be possible to get from any page on your website to any other page by following one or more hyperlinks.
- Your website must include at least one list (ordered or unordered), at least one table, and at least one image.
- Your website must have at least one stylesheet file.
- Your stylesheet(s) must use at least five different CSS properties, and at least five different types of CSS selectors. You must use the #id selector at least once, and the .class selector at least once.
- Your stylesheet(s) must include at least one mobile-responsive @media query, such that something about the styling changes for smaller screens.
- You must use Bootstrap 4 on your website, taking advantage of at least one Bootstrap component, and using at least two Bootstrap columns for layout purposes using Bootstrap’s grid model.
- Your stylesheets must use at least one SCSS variable, at least one example of SCSS nesting, and at least one use of SCSS inheritance.


## Books
A app that utilizes goodreads API to search for book reviews/avg review count. Also gives you the ability to review a book/edit yours. You can also see your own reviews and also has an APi to consume data from.
The book covers is also pulled from the internet archive. The user can edit their own reviews from within their control panel or the reviews page.

For full details read the README.md in the books folder.
Uses PostgresSQL+SQLAlchemy+Flask

(Youtube Demo)[https://www.youtube.com/watch?v=jfqE9EjYJ-g]

All code beyond the external libraries I used and the CSV file for the books were hand-written for these assignments thus all code is licensed under the MIT license.


## Flack
A project to recreate something much simpler but similar to Slack/Discord/other chat applications. All of the chat is done via socketio and is databaseless. 
It's all done in Flask+SocketIO with styling by bootstrap.

For a full rundown go to the flack folder and read the readme there.
(Youtube Demo)[https://www.youtube.com/watch?v=PtXNmDIl2lQ]

#The 2020 folder
In the 2020 folder is all of the projects that are for the current version of the course. Don't utilize them for your own work as they are not open-sourced and thus I don't know what license they would be under. Further don't cheat by utilizing my work in your own project.


## 2020 The folder with current assignments Not F/LOSS
These are all Django applications that use sqlite mostly.
### Mail
A basic email app(think gmail but paired down).

(Youtube Demo)[https://www.youtube.com/watch?v=fI2cAQI1fG8]

### Network
A Twitter-like social network.
(Youtube Demo)[https://www.youtube.com/watch?v=LKbzbDpdctc]

### Wiki
A wikipedia like site where the user utilizes markdown for formatting the pages.
No version control is done for pages though.
(Youtube Demo)[https://www.youtube.com/watch?v=5D5pMcwMZUs]

# Capstone
This folder contains my capstone project. As it is all my own code it is fully open source and licensed under the LGPLv3.

The capstone implements a basic shell of a CTF platform. No highscores right now, nor point tracking in it's current form. But it is mainly there because the challenges can be generated programmatically and updated accordingly. The whole site can(mostly) be done w/o requiring a refresh. 

### Libraries/technologies
Django, Scrypt, SQLite*, Modern JavaScript(fetch,let,const, foreach, in etc), jQuery, Bootstrap5(CSS/JS), Python, Sympy.

#### Challenges
There are RSA based attacks
	- Hastaad Broadcast Attack, Common Modulus, Blind Signature Attack/Signature Forgery, Keys vulnerable to Fermat's Near Prime Factorization Attack
Also the Hill Cipher
	- Just the 2x2 variant, has 2 varities. One where the user is given the key the other where they're given a crib.
Everyone's Favorite FizzBuzz
	- 2 varities but both require the same basic thinking of a fizzbuzz challenge.
Affine Cipher
	- The same as hill as far as one has the key given to the person and the other they are only given the crib.

### UX Features
- The modal dialogues all stack upon eachother in exact order.
- Uses modal dialogues for modifying challenges/getting information
- The frontend utilizes an API to get access to hints/challenges and the admin page uses the same api.
- Fetch is used for getting all assets/api requests.
- Local content is updated upon a submit if it's successful so that the local state is the same as the server.
- Alerts are shown if the user gets a flag wrong and then it's removed.
- Everything is labeled with "aria" attributes and when state is updated the attributes are also updated(to help screen readers).
- The whole thing is mobile responsive via Bootstrap and also making sure that all elements scale accordingly

### Security
- Everything's done with Models
- CSRF for all posts.
- All user passwords are stored via ScryptPasswordHasher(a new hasher I wrote that utilizes scrypt)
- All passwords have to meet a minimum strength requirement via ZXCVBN for the password to be submittable
	- The minimum strength required where it would take 10**8 guesses to get their password.
	
For more details go to the capstone_project folder and read the readme there.
(Youtube Demo)[https://www.youtube.com/watch?v=mhvTJmAPKCM]
