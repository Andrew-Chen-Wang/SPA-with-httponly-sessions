# SPA with httpOnly Cookie Sessions

### NOTE! Changing to new "main" branch on March 1st because of BETTER METHOD

According to [Issue #3](https://github.com/Andrew-Chen-Wang/SPA-with-httponly-sessions/issues/3),
a better way to do this to increase development time is to use
sessions for production and JWT for local. Currently, Django-webpack-loader and this
repository uses some form of bundling the React JS which
makes development time really slow.

In essence, use SimpleJWT during development by delivering from
your Node server at port 3000. Then during development,
disable SimpleJWT (if you're lazy, you can add SimpleJWT
to DRF authentication classes via `DEBUG` attr). Please take a look
at our template repositories at SimpleJWT for an example
of development mode; this repository will stay as
production mode. Your React app will know if it's DEBUG
mode since you can use template variables (i.e. `{{ settings.DEBUG }}`)
in the React HTML file and put it as a JSON script:

```html
<script type="application/json" id="debug">DEBUG="{{ settings.DEBUG }}"</script>
```

When you access DEBUG, check if the string says `{{ settings.DEBUG }}` or `"false"`
since both will be strings.

What we could do is use JWT during development mode
to take advantage of React hot-reloading via the Node server
(as in it's running on localhost:3000). Then, we
can take advantage of the GitHub Action deploying to
GitHub Pages CDN so that when `DEBUG=False`, we
can take advantage of SessionMiddleware.

The reason for this difference is that
a browser-unsafe stateless authorization and browser-safe
stateful authorization is regarding development speed. We use
httpOnly cookies for the sake of a XSS event. Regardless
if you're developing or in production, you can test for or
someone may perform XSS; but when you're testing, you won't
necessarily be trying to steal cookies, only the XSS in general.
The only thing that matters is that in your production environment,
when XSS happens, your session cookies are safe.

If you have a JS and Django repository, then you need two GitHub actions:
deploy static files to your CDN at GitHub pages and another for
deploying the files that were in your urls.py (i.e. the HTML file
and the other build files that aren't in that subdirectory) to your
Django repository.

More details are in [Issue #3](https://github.com/Andrew-Chen-Wang/SPA-with-httponly-sessions/issues/3).

---

Create a JS SPA with a non-JS backend using the most secure
method of authorization for browsers: httpOnly cookie, 
server-backed sessions.

All other tutorials use an insecure method of setting session
or JWT tokens in the JS via some REST API for login. Don't
do it anymore. Prone to XSS.

By: [Andrew Chen Wang](https://github.com/Andrew-Chen-Wang)

Created On: 14 January 2021

Finished: 5 Hours later, 15 January 2021. Friend told me to sleep about 2 hours ago... she was definitely right. Shoulda listened honestly...

Brought to you by: [Velnota](https://velnota.com/)

---
### Quick Intro

If you're a Python/Ruby backend developer and dealt with JS frontend,
you've dealt with non-httpOnly-cookie JWT authorization before.
To me, it's not safe, prone to XSS, kinda beefy, etc. This tutorial will teach
you how to use httpOnly cookie sessions instead.

For a quick demo, go to [https://acwpython.pythonanywhere.com/authenticated/](https://acwpython.pythonanywhere.com/authenticated/)
to view the cookies sessionid and csrftoken set by the server using
a React frontend (we logged on for you).

For Djangonauts, you'll still be able to use context variables
like `request.user.is_authenticated` to determine whether a user
is authenticated.

---
# Abstract

JS SPAs are notorious for a variety of reasons,
one of which many can agree on: security! Mostly XSS.

This monolithic repository should be helpful for everyone looking
to work on an SPA using Node and a backend service
that isn't running Node (e.g. Ruby or Python backends).
The reason we have to use something like a JWT
stateless authorization is because we're unable to
deliver the "compiled" React app via our backend.

The solution? Compile it and set it in your static directory!

I'll be using Django today, but the steps are practically the
same for most backend services.

Using Django session middleware with React.
Using sessions is more secure, smaller, and
honestly better when it comes to browsers.
Additionally, the most important part is that
**httpOnly flag** is set. So let's implement it.

---
## Setup for Your SPA/React

I'm using React because why not. You can use whatever you want;
just make sure it can auto-reload since we're developers that
want to just have stuff immediately done.

We're also going to use GitHub pages as our CDN to host the static files.
If you want yours to be in a private repository and/or hosted
by Amazon S3 or another CDN provider, it's probably going to be
the same steps.

1. Assuming you're at the root directory, 
   create your React app using `npx create-react-app my-app`.
   Then run `npm install npm-watch --save-dev`.
2. Go to your React app's `.gitignore` file. Replace `/build`
   with `!/build` and then add `/build/static`.
3. Go to `package.json` and add:
   
```json
{
   // other properties
   "watch": {
      "build": "src/"
   },
   "scripts": {
      // other scripts
      "watch": "npm-watch"
   }
}
```

4. Create another new repository to host the built static files.
   I chose to create a new repository because I understand people
   want a private backend. If you published both in one repository,
   then your gh-pages branch would expose your backend.
5. Copy the GitHub action in `.github/workflows`. Rename all instances of
   `my-app` to your projects, and I have set up an external repo. If you
   need to change that because you want to use one repository,
   [ref this](https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-deploy-to-external-repository-external_repository).
   What this GitHub action does is cd into 
   your React app, test and build it, and then push
   it to that new repository. In that new repository, we're going
   to use GitHub Pages for deployment, but you can basically
   do the same thing as everyone else and host it somewhere
   else using your own automated deployment scripts.
6. Follow this [tutorial](https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-create-ssh-deploy-key)
   to create your "deploy keys" to the other repository. Your deploy
   key goes into the static repository, and your private key goes in your
   backend/monolithic repo. Like this one.
7. Go to your index.html and remove all places that specify %PUBLIC_URL%
   since those go along with your manifest.json file. Read the note
   left in the file to learn more.
8. Finally, run: `npm run watch`. Now, while you're developing your 
   frontend or backend, everything should just auto build. You may 
   need to save your JS files with some hot key like `Ctrl + s` or 
   `Cmd + s` to reload though (like with Python files for Django).

---
## Setup for Backends

The point of this is to configure a template and static directory
on Django. If you're using something like Ruby on Rails, the
steps are similar in that you want a static directory.

1. Generate your Django app
2. Set your template directory to be `BASE_DIR / "my-app" / "build"`.
   For others who don't understand, this template directory is pointing
   at the React build/ directory. It basically tells Django (in this case)
   to look for all your HTML files here.
3. I've created a template view in the "public" app for every root file in the 
   `build/` directory. This does NOT include `build/static/`. So whatever 
   backend you're using, in your index page (i.e. relative URL "/"), just 
   send that index.html file. For the rest, if a URL points to "/favicon.ico",
   make an endpoint for it, too.
4. Mandatory: Use pre-commit. If you're not using requirements.txt, figure
   out how to get pre-commit. It's not only vital that you lint your projects
   but also that you **build your SPA** to prepare for committing. This is because
   during development, your PUBLIC_URL is pointed towards your localhost. The pre-commit
   will set up your index.html file by pointing PUBLIC_URL to your CDN. So figure
   out how to install it preferably with your backend's language, not npm.
5. You can take a look at the .pre-commit-config.yaml file as a guide. Then, 
   do `pre-commit install` then commit and push! The pre-commit is
   performing one last React build so that your deployment is
   up-to-date with your API.
6. Bonus: if you're on Django, I've created a user after you do
   `python manage.py migrate`. If you head to `/authenticated/`, you'll find your
   sessionid and csrftoken set with httpOnly flag on.
   
If you don't want to use pre-commit, just remember to always
run `export PUBLIC_URL=https://your-cdn.github.io/repo && npm run build`

To test that this is working, `pip install gunicorn`
and then run `gunicorn django_session_react.wsgi` and load `127.0.0.1:8000`
(this way, we're using our production settings file).
This is basically Python's version of quick deploying; I don't know about Rails.
To test that the sessions are working, go to the URL at `/authenticated/`
and find the httpOnly cookie that says `sessionid`.

Here's my demo: [https://acwpython.pythonanywhere.com/authenticated/](https://acwpython.pythonanywhere.com/authenticated/)

---
### FAQ

> Why only non-JS backends?

[Here's a clue](https://reactjs.org/docs/create-a-new-react-app.html#nextjs).
What most developers do is host some server/CDN that
delivers the HTML file with the built React app.
Then their backend is just a huge API. We can't set server-backed
session httpOnly cookies since React is not designed to do backend
chores. The browser requests [https://velnota.com](https://velnota.com/)
and you'll hit a CDN that'll return one HTML file.

> Constantly rebuilding takes a long time

The solution would actually be to use the very thing I said is dangerous:
stateless authorization using JWTs! Although, if you use sessions like
crazy, then this isn't an option.

Then why are we still using GitHub pages? This is because they can host
the React built **static files**, i.e. the compressed react-app, on the
gh-pages branch.

> Prove that session cookie is set

Follow those deployment instructions, head to your website at the relative
url of `/authenticated/`, and you'll find sessionid and csrftoken.
You don't even need to do the PUBLIC_URL environment variable,
and it'll still work. Also you can see that httpOnly is set.

> Well, how do users login if it's not by API?

In your public/index.html file, add a context variable from
your server's templating engine that specifies whether the
requesting user is authenticated or not. That way, React
can decide based on that single React script. In Django,
you can use `json_script` with the `request.user.is_authenticated`
variable. That way, in JS, you can do
`JSON.parse(document.getElementById("ID")).data` to determine
if a user is authenticated.

For your login page, you should do a REAL post request to
the server instead of using Fetch or some REST API (perhaps
using a form tag with method POST).
Every time your user logs in, you have to manually refresh the
page. Don't worry; your static files/React JS files are
cached in the browser, so no performance loss.

Here's the demo: [http://acwpython.pythonanywhere.com/authenticated/](http://acwpython.pythonanywhere.com/authenticated/)

---
### License and Credit

Licensed under the Apache 2.0 library

Thanks PythonAnywhere for hosting this web app demo.

Inspired by [React-GH-Pages repo](https://github.com/gitname/react-gh-pages)
and my absolute hated over Issue #71 and PR #157 at one of the
repositories I maintain,
[django-rest-framework-SimpleJWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt).

I would also like to thank my boredom and procrastination of
schoolwork that just said F it, let's do this.
