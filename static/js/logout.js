// Assuming you use express-session
const express = require('express');
const session = require('express-session');
const app = express();

app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: true
}));

// Logout route
app.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            return res.redirect('/dashboard'); // Or wherever you want to redirect on error
        }
        res.redirect('/login.html');
    });
});

document.getElementById('logout').addEventListener('click', function() {
    window.location.href = '/logout';  // Redirects to the logout route
});
