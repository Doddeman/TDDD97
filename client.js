displayView = function(view){
 document.getElementById("clientviewer").innerHTML = view;
};
window.onload = function(){
	//localStorage.removeItem('token');
    welcomeview  = document.getElementById('welcomeview').innerHTML;
    profileview  = document.getElementById('profileview').innerHTML;
	if(localStorage.getItem('token') !== null && localStorage.getItem('token') !== undefined){
		displayView(profileview);
    showHomePanel();
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
		var response = serverstub.signIn(userName, passwordIn);
    if(response.success){
        localStorage.setItem('token', response.data);
        console.log("token: " + localStorage.getItem('token'));
        console.log(response.message);
        displayView(profileview);
        showHomePanel();
    }
    else{
      document.getElementById('signInMessage').style.color = 'red';
      document.getElementById("signInMessage").innerHTML = "Invalid login";
    }
		return response.success;
	}
};

 function signUp(){
	var passwordUp = document.getElementById("passwordUp").value;
	var repeat = document.getElementById("repeat").value;

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
    var response = serverstub.signUp(user);
    document.getElementById("signUpMessage").innerHTML = response.message;
    return response.success;
	}
};

/*FUNCTIONS FOR ACCOUNT PANEL*/
function changePassword(){

  var oldPassword = document.getElementById('oldPassword').value;
  var newPassword = document.getElementById('newPassword').value;
  var newPasswordRpt = document.getElementById('newPasswordRpt').value;
  var token = localStorage.getItem('token');
  document.getElementById('changeMessage').style.color = 'red';
  if(newPassword.length < 6){
    document.getElementById('changeMessage').innerHTML = "New password too short";
  }
  else if(newPassword != newPasswordRpt){
    document.getElementById('changeMessage').innerHTML = "New passwords does not match";
  }
  else {
    var changedStatus = serverstub.changePassword(token, oldPassword, newPassword);
    if(changedStatus.success){
      document.getElementById('changeMessage').style.color = 'green';
    }
    document.getElementById('changeMessage').innerHTML = changedStatus.message;
  }
};

function signOut(){
  var token = localStorage.getItem('token');
  var response = serverstub.signOut(token);
  localStorage.removeItem('token');
  displayView(welcomeview);
};

/*FUNCTIONS FOR HOME PANEL*/
function getUserInfo(){
  var token = localStorage.getItem('token');
  var userData = serverstub.getUserDataByToken(token);
  document.getElementById('uName').innerHTML = userData.data.firstname;
  document.getElementById('uLastname').innerHTML = userData.data.familyname;
  document.getElementById('uGender').innerHTML = userData.data.gender;
  document.getElementById('uCity').innerHTML = userData.data.city;
  document.getElementById('uCountry').innerHTML = userData.data.country;
  document.getElementById('uEmail').innerHTML = userData.data.email;
};

function updateWall(){
  var token = localStorage.getItem('token');
  if(document.getElementById('homePanel').style.display == 'flex'){
    var messages = serverstub.getUserMessagesByToken(token);
    document.getElementById('homeWall').innerHTML = "";
    for(var i = 0; i < messages.data.length; i++){
      console.log(messages.data[i].content);  
      document.getElementById('homeWall').innerHTML += messages.data[i].writer += ": ";
      document.getElementById('homeWall').innerHTML += messages.data[i].content += "</br>";
    }
  }
  else{
    var email = document.getElementById('findEmail').value;
    var messages = serverstub.getUserMessagesByEmail(token, email);
    document.getElementById('browseWall').innerHTML = "";
    for(var i = 0; i < messages.data.length; i++){
      console.log(messages.data[i].content);  
      document.getElementById('browseWall').innerHTML += messages.data[i].writer += ": ";
      document.getElementById('browseWall').innerHTML += messages.data[i].content += "</br>";
    }
  }
}
function postToWall(){
  var token = localStorage.getItem('token');
  if(document.getElementById('homePanel').style.display == 'flex'){
    var userData = serverstub.getUserDataByToken(token);
    var email = userData.data.email;
    var message = document.getElementById("homeTextArea").value;
  }
  else{
      var email = document.getElementById('findEmail').value;
      var message = document.getElementById("browseTextArea").value;
  }
  var response = serverstub.postMessage(token, message, email);
  console.log(response.message);
  
}

/*FUNCTIONS FOR BROWSE PANEL*/
function searchUser(){
  var token = localStorage.getItem('token');
  var searchEmail = document.getElementById('findEmail').value;
  var response = serverstub.getUserDataByEmail(token,searchEmail);

  if(!response.success){
    document.getElementById('searchMessage').style.color = 'red';
  }else {
    document.getElementById('uName2').innerHTML = response.data.firstname;
    document.getElementById('uLastname2').innerHTML = response.data.familyname;
    document.getElementById('uGender2').innerHTML = response.data.gender;
    document.getElementById('uCity2').innerHTML = response.data.city;
    document.getElementById('uCountry2').innerHTML = response.data.country;
    document.getElementById('uEmail2').innerHTML = response.data.email;
    document.getElementById('displayUser').style.display = 'flex';
    document.getElementById('displayWall').style.display = 'flex';
    document.getElementById('displayText').style.display = 'flex';
    document.getElementById('searchMessage').style.color = 'green';
  }
  document.getElementById('searchMessage').innerHTML = response.message;
};

/*FUNCTIONS FOR SHOWING A PANEL*/
function showHomePanel(){
  document.getElementById('homeTab').style.backgroundColor = 'DeepPink';
  document.getElementById('browseTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('accountTab').style.backgroundColor = 'darkmagenta';

  document.getElementById('homePanel').style.display = 'flex';
  document.getElementById('browsePanel').style.display = 'none';
  document.getElementById('accountPanel').style.display = 'none';
  getUserInfo();
};

function showBrowsePanel(){
  document.getElementById('homeTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('browseTab').style.backgroundColor = 'DeepPink';
  document.getElementById('accountTab').style.backgroundColor = 'darkmagenta';

  document.getElementById('homePanel').style.display = 'none';
  document.getElementById('browsePanel').style.display = 'flex';
  document.getElementById('accountPanel').style.display = 'none';
};

function showAccountPanel(){
  document.getElementById('homeTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('browseTab').style.backgroundColor = 'darkmagenta';
  document.getElementById('accountTab').style.backgroundColor = 'DeepPink';

  document.getElementById('homePanel').style.display = 'none';
  document.getElementById('browsePanel').style.display = 'none';
  document.getElementById('accountPanel').style.display = 'flex';
};
