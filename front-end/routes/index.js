const express = require('express');
const mongoose = require('mongoose');
const { body, validationResult } = require('express-validator/check');

const router = express.Router();
const Registration = mongoose.model('Registration');
const Tweets = mongoose.model('Tweets');

router.get('/', (req, res) => {
    res.render('home', { title: 'Home Page' });
});


router.get('/registrations', (req, res) => {
    Registration.find()
      .then((registrations) => {
        res.render('index', { title: 'Listing registrations', registrations });
      })
      .catch(() => { res.send('Sorry! Something went wrong.'); });
  });

router.get('/search', (req, res) => {
    // Tweets.find({priority: "Low"}).project({postID:1})
    Tweets.where({'priority': 'Low'})
    .then((tweets) => {

        // var arr = [];
        // for(var i= 0; i < tweets.length; i++){
        //     var url= "https://twitter.com/anybody/status/";
        //     var tweet_id= tweets[i][postID];
        //     url +=tweet_id;
        //     arr.push(url);
        // }
        

        res.render('search', { title: 'Listing tweets', tweets, arr });
      })
      .catch(() => { res.send('Sorry! Something went wrong.'); });
  });


router.get('/home', (req, res) => {
   
    res.render('home', { title: 'Home Page' });
        
});

// router.get('/search', (req, res) => {
   
//     res.render('search', { title: 'Search Page' });
        
// });

router.get('/categories', (req, res) => {
   
    res.render('categories', { title: 'Categories Page' });
        
});

router.post('/', (req, res) => {
   
    res.render('search', { title: 'Search Page' });
        
});

// router.post('/',
//   [
//     body('name')
//       .isLength({ min: 3 })
//       .withMessage('Please enter a name'),
//     body('email')
//       .isLength({ min: 1 })
//       .withMessage('Please enter an email'),
//   ],
//   (req, res) => {
//     const errors = validationResult(req);

//     if (errors.isEmpty()) {
//         const registration = new Registration(req.body);
//         registration.save()
//           .then(() => { res.send('Thank you for your registration!'); })
//           .catch(() => { res.send('Sorry! Something went wrong.'); });
//     } else {
//       res.render('form', {
//         title: 'Registration form',
//         errors: errors.array(),
//         data: req.body,
//       });
//     }
//   }
// );

module.exports = router;