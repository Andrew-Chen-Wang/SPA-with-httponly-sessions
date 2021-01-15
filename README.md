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

We're also going to use GitHub pages as our CDN to host the frontend.
If you want yours to be in a private repository and/or hosted
by Amazon S3 or another CDN provider, it's probably going to be
the same steps.

1. Create your React app using `npx create-react-app my-app`
2. Add a CNAME file in your `public` folder
   with a dedicated subdomain like main-static.velnota.com
3. Follow this tutorial: [React-GH-Pages repo](https://github.com/gitname/react-gh-pages)
4. Create a new repository to host the built static files.
5. Copy the GitHub action in `.github/workflows`. What this GitHub
   action does is cd into your React app, build it, and then push
   it to that new repository. In that new repository, we're going
   to use GitHub Pages for deployment, but you can basically
   do the same thing as everyone else and host it somewhere
   else using your own automated deployment scripts.

---
## Setup for Backends

The point of this is to configure a template and static directory
on Django. If you're using something like Ruby on Rails, the
steps are similar in that you want a static directory.

1. Generate your Django app
2. Add ~~`base.html` and `index.html`~~ to your OWN templates folder. 
   FIXME I think we're just gonna be stuck with the React index.html
   ~~I still firmly believe in the `base.html` file because you
   could still have static pages that need the same navigation
   bar.~~ Then again, I've never actually programmed an SPA, so
   let me know if that's wrong :P
3. Add a static directory. This is where you typically store 
   your projects' images, JS, and CSS files (this isn't a media
   directory where users can store media files like images). For Django:
   
FIXME Need to write a script to get this automated build to
link or just copy to the template folder...

```python
STATICFILES_DIRS = [
    BASE_DIR / "my-app" / "build" / "static"
]
```

FIXME Need different settings for local and production
since our static url is going to be pointed to that subdomain.

where that string is just the path from the top directory to
the build of your React app.

4. Mandatory: Use pre-commit. If you're not using requirements.txt, figure
   out how to get pre-commit. It's vital that you lint your projects
   but also that you **build your SPA** to prepare for committing. 
5. Do `pre-commit install` and commit then push! The pre-commit is
   performing one last build then copying the index.html file to
   your template folder.

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
