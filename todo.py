# TODO:
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
- utilize SuccessMessageMixin
- pagination for all listviews
- filter for projects listing pages (use django-filters) (filter)


- base view: All Projects Done
-- sub class: my projects Done
-- sub class: subscribe projects Done

- developer approval (approve from super admin)
----- default active false
----- message display to developer that we see your registration .....

- form validation for developer registration page and emplement it client/server side
- implement developer field in the project create form
- fix base.html and toolbar as we agreed

- new project form
--- Step1ProjectCreateView(CreateView) will use Step1ProjectForm
--- ProjectImagesView(CreateView) will use ProjectImageForm
----- List of Images as context
-----
--- ProjectPhasesView(CreateView) will use ProjectPhaseForm
----- List of Phases as context
-----

"""
