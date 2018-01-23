displayView = function(view){
 document.getElementById("clientviewer").innerHTML = view;
};
window.onload = function(){
	localStorage.removeItem('token');
    welcomeview  = document.getElementById('welcomeview').innerHTML;
    profileview  = document.getElementById('profileview').innerHTML;
	if(localStorage.getItem('token') !== null && localStorage.getItem('token') !== undefined){
		displayView(profileview);
		console.log("profile, token: " + localStorage.getItem('token'));
	}
	else{
	displayView(welcomeview);
	console.log("welcome, token: " + localStorage.getItem('token'));
	}
};


function signIn(){
	var userName = document.getElementById("userName").value;
	var passwordIn = document.getElementById("passwordIn").value;
	if(passwordIn.length < 6){
		document.getElementById('message').style.color = 'red';
		document.getElementById("message").innerHTML = "Password must be at least 6 letters";
		return false;
	}
	else{
		var token = serverstub.signIn(userName, passwordIn).data;
		localStorage.setItem('token', token);
		console.log("token: " + localStorage.getItem('token'));
		displayView(profileview);
		console.log(serverstub.signIn(userName, passwordIn).success);
		return true;
	}
};

 function signUp(){
	var passwordUp = document.getElementById("passwordUp").value;
	var repeat = document.getElementById("repeat").value;

	if (passwordUp != repeat){
		document.getElementById('message2').style.color = 'red';
		document.getElementById("message2").innerHTML = "Password does not match";
		return false;
	}
	else if(passwordUp.length < 6){
		document.getElementById('message2').style.color = 'red';
		document.getElementById("message2").innerHTML = "Password must be at least 6 letters";
		return false;
	}
	else{
		var user = {
			'email': document.getElementById("email").value,
			'password': document.getElementById("passwordUp").value,
			'firstname': document.getElementById("firstName").value,
			'familyname': document.getElementById("lastName").value,
			'gender': document.getElementById("gender").value,
			'city': document.getElementById("city").value,
			'country': document.getElementById("country").value,
		}
		serverstub.signUp(user);
		console.log(serverstub.signUp(user).success);

		return true;

	}
};

/*FUNCTIONS FOR ACCOUNT PANEL*/
function changePassword(){
  var oldPassword = document.getElementById('oldPassword').value;
  var newPassword = document.getElementById('newPassword').value;
  var token = localStorage.getItem('token');
  var changedStatus = serverstub.changePassword(token, oldPassword, newPassword);
  //Fixa alla möjliga felmeddelanden
  if(newPassword.length < 6){
    //console.log("Too short");
    document.getElementById('message3').style.color = 'red';
  }
  else {
    if(changedStatus.success == false){
      console.log("Could not change password");
    }
    else {
      console.log("Password changed")
    }
  }
};

function signOut(){
  var token = localStorage.getItem('token');
  serverstub.signOut(token);
  localStorage.removeItem(token);
  displayView(welcomeview);
};
/*FUNCTIONS FOR HOME PANEL*/
function getUserInfo(){
  var token = localStorage.getItem('token');
  var userData = serverstub.getUserDataByToken(token);
  document.getElementById('uName').innerHTML = userData.data.firstname;
  document.getElementById('uLastname').innerHTML = userData.data.lastname;
  document.getElementById('uGender').innerHTML = userData.data.gender;
  document.getElementById('uCity').innerHTML = userData.data.city;
  document.getElementById('uCountry').innerHTML = userData.data.country;
  document.getElementById('uEmail').innerHTML = userData.data.email;
};
/*FUNCTIONS FOR BROWSE PANEL*/
function searchUser(){
  var token = localStorage.getItem('token');
  var searchEmail = document.getElementById('findEmail').innerHTML;
  var searchedUser = serverstub.getUserDataByEmail(token,searchEmail);
  //Sätt all profildata, fixa felmeddelande om inte användare finns
};
/*FUNCTIONS FOR SHOWING A PANEL*/
function showHomePanel(){
  document.getElementById('homeTab').style.backgroundColor = 'mediumBlue';
  document.getElementById('browseTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('accountTab').style.backgroundColor = 'darkmagenta';

  document.getElementById('homePanel').style.display = 'block';
  document.getElementById('browsePanel').style.display = 'none';
  document.getElementById('accountPanel').style.display = 'none';
};

function showBrowsePanel(){
  document.getElementById('homeTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('browseTab').style.backgroundColor = 'mediumblue';
  document.getElementById('accountTab').style.backgroundColor = 'darkmagenta';

  document.getElementById('homePanel').style.display = 'none';
  document.getElementById('browsePanel').style.display = 'block';
  document.getElementById('accountPanel').style.display = 'none';
};

function showAccountPanel(){
  document.getElementById('homeTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('browseTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('accountTab').style.backgroundColor = 'mediumblue';

  document.getElementById('homePanel').style.display = 'none';
  document.getElementById('browsePanel').style.display = 'none';
  document.getElementById('accountPanel').style.display = 'block';
};
