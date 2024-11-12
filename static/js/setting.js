document.getElementById('profilePicInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profilePic').src = e.target.result;
        }
        reader.readAsDataURL(file);
        saveProfilePicture(file); // Automatically save the picture
    }
});

document.getElementById('personalInfoForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const country = document.getElementById('country').value;
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Create a data object and only add properties that are not empty
    let data = {};

    if (firstName) data.firstName = firstName;
    if (lastName) data.lastName = lastName;
    if (email) data.email = email;
    if (country) data.country = country;

    // Password change logic
    if (newPassword) {
        if (newPassword !== confirmPassword) {
            alert("New password and confirm password do not match!");
            return;
        } else {
            if (!currentPassword) {
                alert("Please enter your current password to update the password.");
                return;
            }
            data.currentPassword = currentPassword;
            data.newPassword = newPassword;
        }
    }

    // Send the updated data to the server
    updatePersonalInfo(data);
});

function updatePersonalInfo(data) {
    // Simulate an API call to save the data
    console.log("Personal info updated", data);
    alert("Changes saved successfully!");
}

function saveProfilePicture(file) {
    // Simulate an API call to save the profile picture
    console.log("Profile picture saved", file);
}

document.getElementById('enable2FA').addEventListener('click', function() {
    send2FACode();
});

document.getElementById('verifyCodeBtn').addEventListener('click', function() {
    const code = document.getElementById('verificationCode').value;
    verify2FACode(code);
});

function send2FACode() {
    // Simulate sending a verification code to the user's email
    console.log("2FA code sent to email");
    document.getElementById('2faSection').style.display = 'block';
}

function verify2FACode(code) {
    if (code === "123456") {  // Dummy code for testing
        alert("Two-factor authentication enabled successfully!");
    } else {
        alert("Invalid verification code. Please try again.");
    }
}
