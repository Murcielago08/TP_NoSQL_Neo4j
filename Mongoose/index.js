const express = require('express');
const connectDB = require('./config/mongodb');
const routes = require('./routes');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

connectDB();

app.use(express.json());
app.use('/api', routes);

app.listen(PORT, () => console.log(`Serveur lancé sur le port ${PORT}`));
