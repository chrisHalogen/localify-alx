function isValidEmail(email) {
  let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email);
}

function isValidUsername(username) {
  let usernamePattern = /^[a-zA-Z]{4,}$/; // Only letters, at least 4 characters
  return usernamePattern.test(username);
}

function isValidInput(input) {
  return isValidEmail(input) || isValidUsername(input);
}

function getQueryParams() {
  let queryParams = {};
  let queryString = window.location.search.substring(1);
  let pairs = queryString.split("&");

  pairs.forEach(function (pair) {
    let [key, value] = pair.split("=");
    if (key) {
      queryParams[decodeURIComponent(key)] = decodeURIComponent(value || "");
    }
  });

  return queryParams;
}
