const express = require('express');
const router = express.Router();

router.use('/profiles', require('./api/profiles'));

module.exports = router;
