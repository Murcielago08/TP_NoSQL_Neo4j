const Profile = require('./model');

exports.getProfiles = async (req, res) => {
    const profiles = await Profile.find();
    res.json(profiles);
};

exports.getProfileById = async (req, res) => {
    const profile = await Profile.findById(req.params.id);
    if (!profile) return res.status(404).json({ msg: "Profil non trouvé" });
    res.json(profile);
};

exports.createProfile = async (req, res) => {
    const { name, email } = req.body;
    const newProfile = new Profile({ name, email });
    await newProfile.save();
    res.status(201).json(newProfile);
};

exports.updateProfile = async (req, res) => {
    const { name, email } = req.body;
    const profile = await Profile.findByIdAndUpdate(req.params.id, { name, email }, { new: true });
    res.json(profile);
};

exports.deleteProfile = async (req, res) => {
    await Profile.findByIdAndDelete(req.params.id);
    res.json({ msg: "Profil supprimé" });
};

exports.addExperience = async (req, res) => {
    const profile = await Profile.findById(req.params.id);
    profile.experience.push(req.body);
    await profile.save();
    res.json(profile);
};

exports.deleteExperience = async (req, res) => {
    const profile = await Profile.findById(req.params.id);
    profile.experience = profile.experience.filter(exp => exp._id.toString() !== req.params.expId);
    await profile.save();
    res.json(profile);
};

exports.addSkill = async (req, res) => {
    const profile = await Profile.findById(req.params.id);
    profile.skills.push(req.body.skill);
    await profile.save();
    res.json(profile);
};

exports.deleteSkill = async (req, res) => {
    const profile = await Profile.findById(req.params.id);
    profile.skills = profile.skills.filter(skill => skill !== req.params.skill);
    await profile.save();
    res.json(profile);
};

exports.updateInformation = async (req, res) => {
    const profile = await Profile.findByIdAndUpdate(req.params.id, { information: req.body }, { new: true });
    res.json(profile);
};
