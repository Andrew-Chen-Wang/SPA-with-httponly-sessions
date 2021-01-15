# SPA with Sessions

Create a JS SPA with a non-JS backend using the most secure
method of authorization for browsers: server-backed sessions.

By: [Andrew Chen Wang](https://github.com/Andrew-Chen-Wang)

Created On: 14 January 2021

Brought to you by: [Velnota](https://velnota.com/)

---
# Abstract

JS SPAs are notorious for a variety of reasons,
one of which many can agree on: security!

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
So let's implement it.

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
5. Add `"homepage": "https://Andrew-Chen-Wang.github.io/spa-with-sessions-static"`
   to your `package.json`, where you should replace `Andrew-Chen-Wang`
   with your GitHub username and replace `spa-with-sessions-static`
   with your new repository's name.
6. Copy the GitHub action in `.github/workflows`. Rename all instances of
   `my-app` to your projects, and I have set up an external repo. If you
   need to change that, ref [this](https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-deploy-to-external-repository-external_repository).
   What this GitHub action does is cd into 
   your React app, test and build it, and then push
   it to that new repository. In that new repository, we're going
   to use GitHub Pages for deployment, but you can basically
   do the same thing as everyone else and host it somewhere
   else using your own automated deployment scripts.
7. Follow this [tutorial](https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-create-ssh-deploy-key)
   to create your "deploy keys" to the other repository.
8. Finally, run: `npm run watch`. Now, while you're developing your 
   frontend or backend, everything should just auto build. You may 
   want to save your JS file to reload though (like with Python files
   for Django).

---
## Setup for Backends

The point of this is to configure a template and static directory
on Django. If you're using something like Ruby on Rails, the
steps are similar in that you want a static directory.

1. Generate your Django app
2. Set your template directory to be `BASE_DIR / "my-app" / "build"`
3. In your production settings, set the static URL to your CDN's URL.
   For me, that was `https://andrew-chen-wang.github.io/spa-with-session-static`.
   Set your `STATICFILES_DIRS` in local settings to point to the
   React static folder that was just built:

```python
STATICFILES_DIRS = [
    BASE_DIR / "my-app" / "build" / "static"
]
```

where that string is just the path from the top directory to
the `build` directory of your React app.

4. Mandatory: Use pre-commit. If you're not using requirements.txt, figure
   out how to get pre-commit. It's not only vital that you lint your projects
   but also that you **build your SPA** to prepare for committing. So figure
   out how to install it preferably with your backend's language, not npm.
5. Adjust build_react_app.py to your language or just other stuff you wanna do.
   Do `pre-commit install` then commit and push! The pre-commit is
   performing one last React build so that your deployment is
   up-to-date with your API.
   
If you don't want to use pre-commit, just remember to always
run `PUBLIC_URL=https://your-cdn.github.io/repo npm run build`

---
### FAQ

> Why only non-JS backends?

[Here's a clue](https://reactjs.org/docs/create-a-new-react-app.html#nextjs).
What most developers do is host some server/CDN that
delivers the HTML file with the built React app.
Then their backend is just a huge API. We can't set server-backed
session cookies since React is not designed to do backend
chores. The browser requests [https://velnota.com](https://velnota.com/)
and you'll hit a CDN that'll return one HTML file.

> Constantly rebuilding takes a long time

The solution would actually be to use the very thing I said is dangerous:
stateless authorization using JWTs! Although, if you use sessions like
crazy, then this isn't an option.

Then why are we still using GitHub pages? This is because they can host
the React built **static files**, i.e. the compressed react-app, on the
gh-pages branch.

---
### License and Credit

Licensed under the Apache 2.0 library

Inspired by [React-GH-Pages repo](https://github.com/gitname/react-gh-pages)
and my absolute hated over PR #71 at one of the
repositories I maintain,
[django-rest-framework-SimpleJWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt).

I would also like to thank my boredom and procrastination of
schoolwork that just said F it, let's do this.
