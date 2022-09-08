# DONE:
"""
#   0- inner class for all choises values
#   1- str funtion to all class
#   2- null , blank for all
#   3 - related name for all classes
#   4 - verbase for all
#   5 - add package for soicial login
#   6 - add plugin phone, mobile number
#   7 - tow factor authentecation
#   8 - localizations - internatioalization
#   9 - Base Views for Auth (Cleint - Developer)
#   10 - crispy forms

# namespacing urls
# fix settings login/logout urls
# base.html with login/logout and welcome message for loggedin users
# 3 views:
#   - list of projects developed by the developer
#   - list of all subscripbed projects (for client)
#   - list of all projects (for public)


- template namespacing Done
- crispy basic setup Done
- media files settings and urls (local) Done
--- designated folder (media)
--- break-down for media sub-folders
- login - logout - logged-in user - links authorized (templatetags)
- base view: All Projects Done
-- sub class: my projects Done
-- sub class: subscribe projects Done

- developer approval (approve from super admin)
----- default active false
----- message display to developer that we see your registration .....
- implement developer field in the project create form
- fix base.html and toolbar as we agreed


- replace objects.get -> objects.get_or_404
- pagination for all listviews
- social login
- google maps
- referral
-- slider or gallery                                                                    Done
-- phases
---- show free phases only for non-subscribed users
---- enable subscription
"""


# TODO:
"""
- can not subscript more than one
- utilize SuccessMessageMixin
- filter for projects listing pages (use django-filters) (filter)                       Later
- form validation for developer registration page and implement it client/server side
- project details view/template                                                          
- add messages to models                                                               testing
--  send messages as email
- tow factor authentication
- payment gateway
- msm gateway


Assigned to Abdullah
- new project form
--- Step1ProjectCreateView(CreateView) will use Step1ProjectForm
--- ProjectImagesView(CreateView) will use ProjectImageForm
----- List of Images as context
-----
--- ProjectPhasesView(CreateView) will use ProjectPhaseForm
----- List of Phases as context
-----
1 - client: display project map
2 - authall interfaces
3 - developer:
    Updates
    
later: get address form leaflet map

- make description files as rich text editor:
--- Normal
--- https://github.com/agusmakmun/django-markdown-editor

"""
# TODO:
""""
Saturday:
* fix alert messages and make them floating -----------------------------------------------------Done
* remove dashboard ------------------------------------------------------------------------------Done
* TRANSLATE ALL STRINGS
* revamp the display of phases in sub-phases in the project page
* Fix the allauth login/signup functionality
* Fix project images
* implement an email notification system (Next step: scalable solution)
* Implement display for update attachements (all file types)
* Implement AJAX pagination for updates
* Fix the search form in home page

Next Week:
* Implement a payment gateway like payfort
* implement an image uploading and thumbnailing plugin

Refactoring:
* create a templatetag to display projects (DRY) and make the projects listing consistent
* create a templatetag to display page titles and reuse it everywhere
* create a templatetag to display upadates

"""