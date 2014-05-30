ShowTown Beta V 1.0.0
=================

Code Documentation
------------------

**account.py** - Contains the password reset workflow.
    
    *Classes*:
        1. Account - Displays the page to accept the email address for password reset.  Sends verification email to user.
        2. PasswordReset - Contains logic to reset the users password.


**activate.py** - Contains the account activation workflow.
    
    *Classes*:
        1. Activate - Receives get request from verification email and sets verifed = true in model.


**calculations.py** (to be deprecated) - Used to calculate various statistics for musicians. Data will be denormailized going forward.
    
    *Classes*:
        1. LikesCount - Calculates likes for musicians.


**find_musicians.py** (future feature) - Will display form to search for musicians for specified parameters.
    
    *Classes*:
        1. FindMusiciansHandler - Currently just displays page.


**follow.py** - Follow & Unfollow musicians workflow.
    
    *Classes*:
        1. FollowHandler - Receives and handles request to follow or unfollow musicians.


**gigs.py** (Future Feature) - All Add, Modify, Delete gigs logic.  Apply to gig logic.
    
    *Classes*:
        1. VenueAddEditGigHandler - Allows venue to add or edit gigs.
        2. DeleteGigHandler - Allows venue to delete gig.
        3. AvailableGigsHandler - Displays availabe gigs in venue pop-up.  Dumps data into JSON.
        4. ApplyWindowHandler - Displays specific gig data and form for musician to apply.
        5. Apply_to_Gig_Handler - Allows musician to apply to specific gig with youtube video.
        6. ApplicantsHandler - Allows venue to either accept or deny musician for gig.


**image_handler.py** - Image rendering engine.
    
    *Classes*:
        1. ImageHandler - Renders images stored in database as .jpg when key is used in url.


**login.py** - Workflow for logging in and out of user account.
    
    *Classes*:
        1. Login - Logs user into account.
        2. Logout - Logs user out of account.


**logout.py** (to deprecate, already contained in login) - log user out of account
    
    *Classes*:
        1. Logout - Logs user out of account.



**main.py** -  Displays main page as well as rendering logic for other static pages
    
    *Classes*:
        1. MainHandler - Displays index.html and logic for random video display / voting.
        2. FaqHandler - Displays FAQ page
        3. PrivacyHandler - Displays Privacy Page
        4. TermsHandler - Displays Terms & Conditions page


**musician.py** - Displays musician profile 
    
    *Classes*:
        1. MusicianHandler - Calculates musician stats and renders page.



**profile.py**  - Displays user specific profile pages
    
    *Classes*:
        1. FanProfileHandler - Displays Fan profile page.
        2. VenueProfileHandler - Displays venue profile page.
        3. VenueProfileApplicantsHandler - Displays applicant data for gig
        4. MusicianProfileHandler - Displays musicians profile page


**signup.py** - Displays signup / modify profile pages
    
    *Classes*:
        1. SignupFanHandler - Displays an interface to edit profile if fan is logged in, otherwise blank signup page.
        2. SignupMusicianHandler - Displays an interface to edit profile if musician is logged in, otherwise blank signup page.
        3. SignupVenueHandler - Displays an interface to edit profile if venue is logged in, otherwise blank signup page.
        4. SignupHandler - Receives post request and provides form validaiton and data requests.



**trending.py** - Displays trending page based on specified parameters
    
    *Classes*:
        1. TrendingHandler - Displays disticnt genres / states and pulls trending data.



**venues.py** - Displays venue specific page, as well as list of venues page.
    
    *Classes*:
        1. VenuesHandler - Displays list of venues.
        2. VenueHandler - Displays individual venue page.



**video_handler.py** - logic for handling videos assigned to musicians.
    
    *Classes*:
        1. UnFeatureHandler - Unfeatures a selected video.
        2. FeatureHandler - Features a selected video and unfeatures all others.
        3. RemoveHandler - Deletes a specified video.
        4. Add Handler - Uploads a new video.



**views.py** - logic for rendering html templates and handling webapp2 requests
    
    *Classes*:
        1. Template - Checks for current user, renders html templates and emails.



**vote_handler.py** - Logic for handling video votes and 'I like this' requests
    
    *Classes*:
        1. LikeHandler - Processes requests to like a video.
        2. VoteHandler - Processes requests to vote on head-to-head contest.


Other Files
-----------

**app.yaml**  - Config file for url routing and library imports


**cron.yaml**  - Config file for automated tasks scheduling.



Current Dependencies - Back End
-------------------------------

1. webapp2 - Request Handler framework
2. jinja2 - HTML templating engine
3. google.appengine.ext: ndb - Google Datastore
4. google.appengine.api: images - Image library similar to PIL.  Used for cropping, scaling, and rendering images.
5. google.appengine.api: urlfetch - API used to request data from other websites.
6. lassie - Python library for scraping content from webpages.  Currently used to pull video data from YouTube and Vimeo
7. requests - Similar to #5, but a 3rd party library.  Currently unused.
8. braintree - Credit card processing library


Current Dependencies - Front End
--------------------------------

1. bootstrap - Framework for fast JS optimization
2. jquery - JS library for consolidated development