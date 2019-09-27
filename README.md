# ESP-Game
A REST API backend for an esp game used for tagging images.

## Gameplay
Let’s suppose we have Player A and Player B. There are 15 questions in the system (i.e. 15 primary images). Each time Player A starts the game, he/she is shown 5 random primary images and secondary images corresponding to the primary image. 

1. Player A selects the matching secondary images for the primary image
2. Player B is shown the same 5 question (i.e same 5 primary image). Player B selects his/her answers.
3. If the answer for Player A and Player B match, both of them get a point else none of them gets the point.

Secondary images for a question are > 1.

## Apps/Dependencies
1. Django REST framework
2. drf-extensions
3. django-cors-headers
4. Pillow

## Assumptions and Working 
1. Each secondary image is associated with only one primary image.
2. Task is generated dynamically for each user and locked. In each task, system always tries to maximize the questions that have 1 answer.
3. If a question receives 2 answers, it is not asked to any other user.
4. A question will not be asked to a user who has already answered it in the past correctly or even incorrectly. By correctly we mean that its answer matched with that of another user for that question and vice versa.
5. Matching answers are kept in the system and question has reached consensus. Therefore it will not be shown to any other user later. Non matching answers are discarded from the system  and will be shown to future users.
6. A user has to mark all the answers properly for questions of the task he/she has undertaken. Incomplete responses are discarded.

## Setup
1. git clone https://github.com/sahibjotsingh/ESP-Game
2. Setup virtual environment in your directory using virtualenv venv
3. Activate venv using venv\Scripts\activate
4. Install Django - pip install django
5. Install Django REST framework - pip install djangorestframework
6. Install drf-nested-routers - pip install drf-extensions
7. Install django-cors-headers - pip install django-cors-headers
8. Install pillow - pip install pillow

Note : Make users and user profiles ie. myuser from the admin panel only. Also insert primary images and their corresponding secondary images through admin panel. A dataset with 6 primary images and their secondary images (2 each) is already populated.

## Endpoints 
* Authenticated
   * GET: /myuser/{myuserId}/get-task/ <br/>
        Returns a group of questions (primary images) with their corresponding secondary images.
   * GET: /myuser/{myuserId}/track-game/match/{secondaryImageId}/ <br/>
        Marks true for secondaryImage being a match of its primary primary image
   * GET: /myuser/{myuserId}/track-game/unmatch/{secondaryImageId}/ <br/>
        Marks false for secondaryImage being a match of its primary image
   * GET: /myuser/{myuserId}/end-task/ <br/>
        Submit answers for questions of this task. 
   * GET: /myuser/{myuserId}/end-game/ <br/>
        End the game ie. discard the responses for questions of task undertaken (if any).
        
## Roadmap
1. Use Django Channels (websocket)
2. Implement Silent Authentication
