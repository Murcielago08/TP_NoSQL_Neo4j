const mongoose = require('mongoose');

const ExperienceSchema = new mongoose.Schema({
    titre: String,
    entreprise: String,
    dates: String,
    description: String
});

const ProfileSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    experience: [ExperienceSchema],
    skills: [String],
    information: {
        bio: String,
        localisation: String,
        siteWeb: String
    }
});

module.exports = mongoose.model('Profile', ProfileSchema);
