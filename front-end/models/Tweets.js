const mongoose = require('mongoose');

const tweetSchema = new mongoose.Schema({
  _id: {
    type: Number,
    trim: true,
  },
  postID: {
    type: Number,
    trim: true,
  },
});
const collectionName = 'training'

module.exports = mongoose.model('Tweets', tweetSchema, collectionName);