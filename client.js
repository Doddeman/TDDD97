displayView = function(view){
 document.getElementById("clientviewer").innerHTML = view;
};
window.onload = function(){
	//localStorage.removeItem('token');
    welcomeview  = document.getElementById('welcomeview').innerHTML;
    profileview  = document.getElementById('profileview').innerHTML;
	if(localStorage.getItem('token') !== null && localStorage.getItem('token') !== undefined){
		displayView(profileview);
		console.log("profile, token: " + localStorage.getItem('token'));
	}
	else{
	displayView(welcomeview);
  //displayView(profileview);
	console.log("welcome, token: " + localStorage.getItem('token'));
	}
};


function signIn(){
	var userName = document.getElementById("userName").value;
	var passwordIn = document.getElementById("passwordIn").value;
	if(passwordIn.length < 6){
		document.getElementById('signInMessage').style.color = 'red';
		document.getElementById("signInMessage").innerHTML = "Password must be at least 6 letters";
		return false;
	}
	else{
    //fråga om serverstub.signin kallas flera gånger...
		var token = serverstub.signIn(userName, passwordIn).data;
		localStorage.setItem('token', token);
		console.log("token: " + localStorage.getItem('token'));
		//displayView(profileview);
		console.log(serverstub.signIn(userName, passwordIn).success);
		return true;
	}
};

 function signUp(){
	var passwordUp = document.getElementById("passwordUp").value;
	var repeat = document.getElementById("repeat").value;
  
  document.getElementById('signUpMessage').style.color = 'red';
	if (passwordUp != repeat){
		document.getElementById("signUpMessage").innerHTML = "Passwords does not match";
		return false;
	}
	else if(passwordUp.length < 6){
		document.getElementById("signUpMessage").innerHTML = "Password must be at least 6 letters";
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
    console.log(serverstub.signUp(user).message);
    //console.log(serverstub.signUp(user).message);
		//console.log(serverstub.signUp(user));


		return true;

	}
};

/*FUNCTIONS FOR ACCOUNT PANEL*/
function changePassword(){
  
  var oldPassword = document.getElementById('oldPassword').value;
  var newPassword = document.getElementById('newPassword').value;
  var newPasswordRpt = document.getElementById('newPasswordRpt').value;
  var token = localStorage.getItem('token');

  if(newPassword.length < 6){
    document.getElementById('changeMessage').innerHTML = "New password too short";
    //return false;
  }
  else if(newPassword != newPasswordRpt){
    document.getElementById('changeMessage').innerHTML = "New passwords does not match";
    //return false;
  }
  else {
    var changedStatus = serverstub.changePassword(token, oldPassword, newPassword);
    document.getElementById('changeMessage').innerHTML = changedStatus.message;
    //return true;
  }
};

function signOut(){

  var token = localStorage.getItem('token');
  alert(serverstub.signOut(token).message);
  serverstub.signOut(token);
  localStorage.removeItem('token');
  //displayView(welcomeview);
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
  var searchedUserData = serverstub.getUserDataByEmail(token,searchEmail);

  if(searchedUserData.success == false){
    console.log("User does not exist!");
  }else {
    document.getElementById('uName2').innerHTML = searchedUserData.data.firstname;
    document.getElementById('uLastname2').innerHTML = searchedUserData.data.lastname;
    document.getElementById('uGender2').innerHTML = searchedUserData.data.gender;
    document.getElementById('uCity2').innerHTML = searchedUserData.data.city;
    document.getElementById('uCountry2').innerHTML = searchedUserData.data.country;
    document.getElementById('uEmail2').innerHTML = searchedUserData.data.email;
  }
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
