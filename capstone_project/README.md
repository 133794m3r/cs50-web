# CTF Club/Capstone Project
This folder contains the Capstone project that I wrote. It has the features listed below and checks all of the boxes required.

If you want to start from a fresh/clean slate. Delete the db.sqlite3 file and then run  ``python mage.py migrate``. I have the migrations already in the DB so that it's in the same state as when I recorded the video.

## Youtube Link
https://www.youtube.com/watch?v=mhvTJmAPKCM

## Major Features
- [x] Utilizes Django
- [x] Uses Multiple Models
- [x] Uses JavaScript on the Front-end
- [x] Uses Python on the backend.
- [x] Completely distinct from other projects from the courses.
- [x] Has multiple different views and templates.
- [x] Mobile Responsive(via BootStrap handling the majority of the theming.)
- [x] Uses PostgreSQL for the database backend.
- [x] Challenges can create files which are then sent to the users.
- [x] Programming challenges give users a test case to try to do.
- [x] AdminView is modified to be ratelimited to avoid having bruteforcing of teh view.
- [x] Login/Registration are rate-limited.
- [x] A basic CAPTCHA for registration is shown and for logins if they were rate-limited is required to be solved. 

## Challenge Generators
- RSA Attacks
	- Hastaad Broadcast Attack via Chinese Remainder Theorem (Just with e=3 to keep the challenge easy)
	- Fermat's Near Prime Factorization Attack
	- RSA Bling Signature Forgery
	- Common Modulus attack via Chinese Remainder Theorem
- FizzBuzz based challenge.
- Affine Cipher
	- Both a keyed and a cribbed varient for students to solve.
- Hill Cipher
	- Same as above a keyed and a cribbed variant. Just a 2x2 matrix for simplicity's sake.
- Unbound Knapsack Algorithm
    - Aka the "master hacker" challenge.
    
### Where to see the Generators
The generators themselves are mostly in the util.py file.

## Math Involved
- Discrete Math
	- Carmachael's Totient function
	- Extended Euclidean Algorithm for use in calculated GCD generalized to work for all integers of the set Z(both a and b).
	- RSA key generators(variable size based upon input so that the key is the minimal size required to keep information from being lost during encryption/decryption)
	- Hastaad's Broadcast Attack via the Chinese Remainder Theorem
	- Common Modulus Attack
	- RSA Blinded Signature Forgery
- Algorithms
    - There's a challenge that is involves the Unbound Knapsack problem.
- Elementary Number Theory(or so I believe)
	- Fermat's factorization method
- Linear Algebra
	- Hill cipher's calculation of the decryption key.

All of the fields of math are best estimates as I have no formal math background and have learned what I know by doing CTF challenges and reading research papers.

## Math folders
The generators are stored within the libctf directory within the ctf_club folder. The solves aren't
included in this distro so that students can't easily solve the challenges.

### Papers explaining the challenges/how to solve them.
The papers for how to solve the challenges is linked below(some of the hints already have them).

[RSA Paper going from General RSA, to all of the challenges I've seen live.](https://github.com/133794m3r/Papers/blob/master/crypto/RSA_LAB_1.pdf)
#### Contents
The paper goes into attacks suchas "e"th root attacks, Hastaad Broadcast with values greater than 3(5 in the papers case), Fermat's Near Prime attack, Common Modulus, Blind Signature Attack, and also includes step-by-step guides explaining how to do them all. The "proofs" section needs work as I am no mathematician and I've tried to explain it somewhat well but I know it could be done better. If one reads that paper after digesting it, they will walk away with the ability to carry out all of the attacks against RSA that are described therein in any CTF challenge.

[Hill Cipher Paper](https://github.com/133794m3r/Papers/blob/master/crypto/HILL_CIPHER.pdf)
#### Contents
That paper goes over the linear algebra required to crack a message enciphered with a hill cipher(the crib is given to the person in the paper) but goes over basic matrix operations required to complete it. It's definitely not textbok quality by any stretch of the imagination.

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
- Everything is ratelimited.
    - The admin view is also wrapped behind a double ratelimit.
    - One for the username and also a second.
    - One for the ip address trying to attack the system.

## Full Feature List
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

The sympy library is utilized for the RSA flags I could've wrote them myself but I decided against it. The pycryptodome package is only required if you want to generate public and private keys in PEM format.
This includes all packages required.
