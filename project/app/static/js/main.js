$(document).ready(function () {
  // Open and close mobile menu

  $("#close-icon, #hamburg").click(() => {
    $("#main-nav").toggleClass("open-nav");
  });

  // Register Script
  $("#register-form").on("submit", function (event) {
    event.preventDefault();
    console.log("Submitting");
    let username = $("#username").val().trim();
    let email = $("#email").val().trim();
    let password = $("#password").val().trim();
    let rePassword = $("#rePassword").val().trim();

    let errors = [];
    // Validate the inputs
    if (username.length < 4 || !/^[a-zA-Z]+$/.test(username)) {
      errors.push(
        "Username must be at least 4 characters long and contain only letters."
      );
    }

    let emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
      errors.push("Invalid email address.");
    }

    let passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$/;
    if (!passwordPattern.test(password)) {
      errors.push(
        "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
      );
    }
    if (password !== rePassword) {
      errors.push("Passwords do not match.");
    }

    // If there are errors, show a notification
    if (errors.length > 0) {
      showNotification("Error", errors.join("<br>"), "error");
      return;
    }

    console.log("No error discovered");

    // Send the data to the Flask endpoint using AJAX
    $.ajax({
      type: "POST",
      url: "/create-new-user", // The Flask endpoint
      contentType: "application/json",
      data: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
      success: function (response) {
        if (response.status === "error") {
          showNotification("Error", response.message, "error");
        } else {
          showNotification(
            "Success",
            "Registration successful! Redirecting to login page...",
            "success"
          );
          setTimeout(function () {
            window.location.href = "/login"; // Redirect to login page
          }, 2000);
        }
      },
      error: function (error) {
        let msg =
          error.status === 409
            ? "Username or email already exists."
            : "An error occurred. Please try again.";
        showNotification("Error", msg, "error");
      },
    });
  });

  // Login Script
  $("#login-form").on("submit", function (event) {
    event.preventDefault();

    let user_input = $("#user_id_data").val().trim();
    let password = $("#password").val().trim();
    let errors = [];

    // Validate the inputs
    if (user_input.length === 0) {
      errors.push("Username or Email is required.");
    } else if (!isValidInput(user_input)) {
      errors.push("Invalid Username or Email.");
    }

    if (password.length === 0) {
      errors.push("Password is required.");
    }

    // If there are errors, show a notification
    if (errors.length > 0) {
      showNotification("Error", errors.join("<br>"), "error");
      return;
    }

    // Send the data to the Flask endpoint using AJAX
    $.ajax({
      type: "POST",
      url: "/log-user-in",
      contentType: "application/json",
      data: JSON.stringify({
        user_input: user_input,
        password: password,
      }),
      success: function (response) {
        if (response.status === "error") {
          showNotification("Error", response.message, "error");
        } else {
          showNotification(
            "Success",
            "Login successful! Redirecting to home page...",
            "success"
          );

          let params = getQueryParams();
          let paramValue = params["next"];
          let destination =
            paramValue === undefined && paramValue !== ""
              ? "/listings"
              : paramValue;

          setTimeout(function () {
            window.location.href = destination; // Redirect to home page
          }, 2000);
        }
      },
      error: function (error) {
        let msg =
          error.status === 401
            ? "Invalid username/email or password."
            : "An error occurred. Please try again.";

        showNotification("Error", msg, "error");
      },
    });
  });

  // Create Business Script
  $("#create-new").on("click", function () {
    // Extract form data
    const name = $("#name").val();
    const address = $("#address").val();
    const city = $("#city").val();
    const state = $("#state").val();
    const zip_code = $("#zip_code").val();
    const phone = $("#phone").val();
    const website = $("#website").val();
    const category = $("#category").val();
    const description = $("#description").val();
    const logo = $("#logo")[0].files[0];
    const cover_photo = $("#cover_photo")[0].files[0];

    // Initialize error messages
    let errors = [];

    // Validate name
    const namePattern = /^[A-Za-z0-9.,' ]{4,}$/;
    if (!namePattern.test(name)) {
      errors.push(
        "Name must be at least 4 characters long and can only contain letters, numbers, commas, periods, spaces, and apostrophes."
      );
    }

    // Validate address
    const addressPattern = /^[A-Za-z0-9. ,]{5,}$/;
    if (!addressPattern.test(address)) {
      errors.push(
        "Address must be at least 5 characters long and can only contain letters, periods, comma, numbers, and spaces."
      );
    }

    // Validate city and state
    const cityStatePattern = /^[A-Za-z. ]{3,}$/;
    if (!cityStatePattern.test(city)) {
      errors.push(
        "City must be at least 3 characters long and can only contain letters, periods, and spaces."
      );
    }
    if (!cityStatePattern.test(state)) {
      errors.push(
        "State must be at least 3 characters long and can only contain letters, periods, and spaces."
      );
    }

    // Validate phone
    const phonePattern = /^\+?\d{1,14}$/;
    if (phone.length > 14 || !phonePattern.test(phone)) {
      errors.push(
        "Phone number must be up to 14 characters long and can only contain digits and optionally start with a +."
      );
    }

    // Validate logo file
    if (logo) {
      const logoSize = logo.size / 1024 / 1024; // Convert bytes to MB
      const allowedLogoTypes = ["image/png", "image/jpeg", "image/jpg"];
      if (!allowedLogoTypes.includes(logo.type)) {
        errors.push("Logo must be a valid PNG, JPG, or JPEG file.");
      } else if (logoSize > 4) {
        errors.push("Logo must not exceed 4MB in size.");
      }
    }

    // Validate cover photo file
    if (cover_photo) {
      const coverPhotoSize = cover_photo.size / 1024 / 1024; // Convert bytes to MB
      const allowedCoverPhotoTypes = ["image/png", "image/jpeg", "image/jpg"];
      if (!allowedCoverPhotoTypes.includes(cover_photo.type)) {
        errors.push("Cover photo must be a valid PNG, JPG, or JPEG file.");
      } else if (coverPhotoSize > 8) {
        errors.push("Cover photo must not exceed 8MB in size.");
      }
    }

    // Show errors if any
    if (errors.length > 0) {
      showNotification("Error", errors.join("<br>"), "error");
      return;
    }

    // Prepare form data for submission
    const formData = new FormData();
    formData.append("name", name);
    formData.append("address", address);
    formData.append("city", city);
    formData.append("state", state);
    formData.append("zip_code", zip_code);
    formData.append("phone", phone);
    formData.append("website", website);
    formData.append("category", category);
    formData.append("description", description);
    if (logo) formData.append("logo", logo);
    if (cover_photo) formData.append("cover_photo", cover_photo);

    $.ajax({
      url: "/listings/create-new-business",
      method: "POST",
      data: formData,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response.status === "success") {
          showNotification("Success", response.message, "success");
          setTimeout(function () {
            window.location.href = "/listings"; // Redirect to the listings page
          }, 2000);
        } else {
          showNotification("Error", response.message, "error");
        }
      },
      error: function (xhr, status, error) {
        showNotification(
          "Error",
          "An error occurred. Please try again later.",
          "error"
        );
      },
    });
  });

  // Delete Action
  $(".listings").on("click", ".delete", function () {
    // Get the business ID from the parent .single-business element
    const businessId = $(this).closest(".single-business").data("id");

    // Send AJAX request to delete the business
    // $.ajax({
    //   url: "/delete-business",
    //   method: "DELETE",
    //   contentType: "application/json",
    //   data: JSON.stringify({ id: businessId }),
    //   success: function (response) {
    //     if (response.status === "success") {
    //       showNotification("Success", response.message, "success");
    //       // Reload the page after showing the notification
    //       setTimeout(function () {
    //         location.reload();
    //       }, 2000);
    //     } else {
    //       showNotification("Error", response.message, "error");
    //     }
    //   },
    //   error: function (xhr, status, error) {
    //     showNotification(
    //       "Error",
    //       "An unexpected error occurred. Please try again.",
    //       "error"
    //     );
    //   },
    // });

    // Confirm the action with the user
    if (confirm("Are you sure you want to delete this business?")) {
      $.ajax({
        url: "/delete-business", // Endpoint URL
        method: "DELETE", // Use DELETE method
        contentType: "application/json",
        data: JSON.stringify({ id: businessId }),
        success: function (response, textStatus, xhr) {
          if (xhr.status === 204) {
            showNotification(
              "Success",
              "Business deleted successfully.",
              "success"
            );
            setTimeout(function () {
              location.reload();
            }, 2000);
          } else {
            showNotification(
              "Error",
              "An unexpected error occurred. Please try again.",
              "error"
            );
          }
        },
        error: function (xhr, status, error) {
          const response = xhr.responseJSON;
          if (response && response.message) {
            showNotification("Error", response.message, "error");
          } else {
            showNotification(
              "Error",
              "An unexpected error occurred. Please try again.",
              "error"
            );
          }
        },
      });
    }
  });

  // Update Action
  $("#update-business").on("click", function () {
    const businessId = $(this).data("id");
    const name = $("#name").val();
    const address = $("#address").val();
    const city = $("#city").val();
    const state = $("#state").val();
    const zipCode = $("#zip_code").val();
    const phone = $("#phone").val();
    const website = $("#website").val();
    const categoryId = $("#category").val();
    const description = $("#description").val();
    const logo = $("#logo")[0].files[0];
    const coverPhoto = $("#cover_photo")[0].files[0];

    const errors = [];

    // Validate inputs
    if (!/^[a-zA-Z0-9\s,.'-]{4,}$/.test(name)) {
      errors.push(
        "Name must be at least 4 characters long and can only contain letters, numbers, spaces, and the following characters: ,.'-"
      );
    }
    if (!/^[A-Za-z0-9. ,]{5,}$/.test(address)) {
      errors.push(
        "Address must be at least 5 characters long and can only contain letterscommas, numbers, spaces, and periods."
      );
    }
    if (!/^[a-zA-Z\s.]{3,}$/.test(city)) {
      errors.push(
        "City must be at least 3 characters long and can only contain letters, spaces, and periods."
      );
    }
    if (!/^[a-zA-Z\s.]{3,}$/.test(state)) {
      errors.push(
        "State must be at least 3 characters long and can only contain letters, spaces, and periods."
      );
    }
    if (!/^\+?\d{1,14}$/.test(phone)) {
      errors.push(
        "Phone number must be up to 14 digits long and can optionally start with a +."
      );
    }
    if (logo && !/\.(png|jpe?g)$/i.test(logo.name)) {
      errors.push("Logo must be a valid PNG, JPG, or JPEG file.");
    }
    if (logo && logo.size > 4 * 1024 * 1024) {
      errors.push("Logo must not be more than 4MB.");
    }
    if (coverPhoto && !/\.(png|jpe?g)$/i.test(coverPhoto.name)) {
      errors.push("Cover photo must be a valid PNG, JPG, or JPEG file.");
    }
    if (coverPhoto && coverPhoto.size > 8 * 1024 * 1024) {
      errors.push("Cover photo must not be more than 8MB.");
    }

    if (errors.length > 0) {
      showNotification("Error", errors.join("<br>"), "error");
      return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("address", address);
    formData.append("city", city);
    formData.append("state", state);
    formData.append("zip_code", zipCode);
    formData.append("phone_number", phone);
    formData.append("website", website);
    formData.append("category_id", categoryId);
    formData.append("description", description);
    if (logo) formData.append("logo", logo);
    if (coverPhoto) formData.append("cover_photo", coverPhoto);

    $.ajax({
      url: `/edit-business/${businessId}`,
      method: "PUT",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        showNotification("Success", response.message, "success");
        setTimeout(function () {
          window.location.href = "/listings";
        }, 2000);
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        if (response && response.message) {
          showNotification("Error", response.message, "error");
        } else {
          showNotification(
            "Error",
            "An unexpected error occurred. Please try again.",
            "error"
          );
        }
      },
    });
  });

  $("#btn-edit-profile").on("click", function () {
    console.log("Clicked");
    let userId = $(this).data("id");
    let username = $("#username").val();
    let email = $("#email").val();
    let isBusiness = $("#is-business").is(":checked");

    // Validate inputs
    let errors = [];

    if (username.length < 4 || !/^[a-zA-Z]+$/.test(username)) {
      errors.push(
        "Username must be at least 4 characters long and contain only letters."
      );
    }

    let emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
      errors.push("Please enter a valid email address.");
    }

    if (errors.length > 0) {
      showNotification("Error", errors.join("<br>"), "error");
      return;
    }

    // Prepare data for AJAX request
    let formData = {
      user_id: userId,
      username: username,
      email: email,
      is_business: isBusiness,
    };

    // Send AJAX request
    $.ajax({
      url: "/edit-profile",
      type: "PUT",
      contentType: "application/json",
      data: JSON.stringify(formData),
      success: function (response) {
        showNotification("Success", "Profile updated successfully!", "success");
        setTimeout(function () {
          window.location.href = "/profile"; // Redirect to login page
        }, 2000);
      },
      error: function (xhr) {
        let errorMessage = "An error occurred: " + xhr.responseText;
        showNotification("Error", errorMessage, "error");
      },
    });
  });

  // Getting data paginated
  function loadBusinesses(page) {
    $.ajax({
      url: "/get-user-paginated-data",
      type: "GET",
      data: { page: page },
      success: function (response) {
        let businesses = response.businesses;
        let totalPages = response.total_pages;
        let currentPage = response.current_page;

        // Update the business listings
        let listingsDiv = $(".listings");
        listingsDiv.empty();
        console.log(businesses.length);

        if (businesses.length === 0) {
          listingsDiv.html("<p>You have no businesses.</p>");
          return;
        }

        $.each(businesses, function (index, business) {
          listingsDiv.append(
            `<div class="single-business" data-id="${business.id}">
            <p class="title">${business.name}</p>
            <p class="category">${business.category}</p>
            <div class="action">
                <a href="/edit-business/${business.id}">Edit</a>
                <button class="delete">Delete</button>
            </div>
        </div>`
          );
        });

        // Update the pagination
        let paginationDiv = $("#pagination");
        paginationDiv.empty();

        if (currentPage > 1) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              (currentPage - 1) +
              '">Previous</button>'
          );
        }

        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
          if (i === currentPage) {
            paginationDiv.append(
              '<button class="page-link active" data-page="' +
                i +
                '">' +
                i +
                "</button>"
            );
          } else {
            paginationDiv.append(
              '<button class="page-link" data-page="' +
                i +
                '">' +
                i +
                "</button>"
            );
          }
        }

        if (totalPages > 5 && currentPage + 2 < totalPages) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              totalPages +
              '">' +
              totalPages +
              "</button>"
          );
        }

        if (currentPage < totalPages) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              (currentPage + 1) +
              '">Next</button>'
          );
        }
      },
      error: function (error) {
        console.error("Error fetching businesses:", error);
      },
    });
  }

  if ($("#listings-page").length) {
    // Initial load
    loadBusinesses(1);

    // Handle pagination click
    $("#pagination").on("click", ".page-link", function () {
      let page = $(this).data("page");
      loadBusinesses(page);
    });
  }

  function truncateString(str, maxLength, append = "...") {
    if (str.length > maxLength) {
      return str.substring(0, maxLength) + append;
    }
    return str;
  }

  function handleImageError(img) {
    img.onerror = null; // Prevents infinite loop
    img.src = "/static/images/placeholder.png";
  }

  // Getting data paginated
  function loadBusinessesbycategory(page, category_id) {
    $.ajax({
      url: "/load-businesses-by-category",
      type: "GET",
      data: { page: page, category_id: category_id },
      success: function (response) {
        let businesses = response.businesses;
        let totalPages = response.total_pages;
        let currentPage = response.current_page;

        // Update the business listings
        let listingsDiv = $(".listing-items");
        listingsDiv.empty();
        console.log(businesses.length);

        if (businesses.length === 0) {
          listingsDiv.html("<p>There are no listings in this category.</p>");
          return;
        }

        $.each(businesses, function (index, business) {
          listingsDiv.append(
            `<div class="single">
                <img src="/static/uploads/${
                  business.cover_photo
                }" alt="single" onerror="this.onerror=null; this.src='/static/images/placeholder.png';">
                <div class="info">
                    <p class="title">${truncateString(business.name, 20)}</p>
                    <p class="description">${truncateString(
                      business.description,
                      50
                    )}</p>
                    <a href="/business-profile/${
                      business.id
                    }" class="learn-more">Learn More >>></a>
                </div>

            </div>`
          );
        });

        // Update the pagination
        let paginationDiv = $("#pagination");
        paginationDiv.empty();

        if (currentPage > 1) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              (currentPage - 1) +
              '">Previous</button>'
          );
        }

        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
          if (i === currentPage) {
            paginationDiv.append(
              '<button class="page-link active" data-page="' +
                i +
                '">' +
                i +
                "</button>"
            );
          } else {
            paginationDiv.append(
              '<button class="page-link" data-page="' +
                i +
                '">' +
                i +
                "</button>"
            );
          }
        }

        if (totalPages > 5 && currentPage + 2 < totalPages) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              totalPages +
              '">' +
              totalPages +
              "</button>"
          );
        }

        if (currentPage < totalPages) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              (currentPage + 1) +
              '">Next</button>'
          );
        }
      },
      error: function (error) {
        console.error("Error fetching businesses:", error);
      },
    });
  }

  if ($("#listings-by-categories-page").length) {
    // Initial load
    let category_id = $("#category-id").val();
    loadBusinessesbycategory(1, category_id);

    // Handle pagination click
    $("#pagination").on("click", ".page-link", function () {
      let page = $(this).data("page");
      loadBusinessesbycategory(page, category_id);
    });
  }

  // Home Page
  function loadBusinessesonhomepage(page) {
    let searchTerm = $("#search-term").val();
    let category = $("#category").val();
    let address = $("#address").val();
    let city = $("#city").val();
    let state = $("#state").val();

    let data = {};
    if (searchTerm) data.search_term = searchTerm;
    if (category != "0") data.category = category;
    if (address) data.address = address;
    if (city) data.city = city;
    if (state) data.state = state;
    data.page = page;

    $.ajax({
      url: "/load-businesses-on-home-page",
      type: "GET",
      data: data,
      success: function (response) {
        let businesses = response.businesses;
        let totalPages = response.total_pages;
        let currentPage = response.current_page;

        let listingsDiv = $(".listing-items");
        let paginationDiv = $("#pagination");

        if (businesses.length === 0) {
          listingsDiv.html("<p>No Listings Found</p>");
          paginationDiv.empty();
          return;
        }

        // Update the business listings
        listingsDiv.empty();

        $.each(businesses, function (index, business) {
          listingsDiv.append(
            `<div class="single">
                <img src="/static/uploads/${
                  business.cover_photo
                }" alt="single" onerror="this.onerror=null; this.src='/static/images/placeholder.png';">
                <div class="info">
                    <p class="title">${truncateString(business.name, 20)}</p>
                    <p class="description">${truncateString(
                      business.description,
                      50
                    )}</p>
                    <a href="/business-profile/${
                      business.id
                    }" class="learn-more">Learn More >>></a>
                </div>

            </div>`
          );
        });

        // Update the pagination
        paginationDiv.empty();

        if (currentPage > 1) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              (currentPage - 1) +
              '">Previous</button>'
          );
        }

        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
          if (i === currentPage) {
            paginationDiv.append(
              '<button class="page-link active" data-page="' +
                i +
                '">' +
                i +
                "</button>"
            );
          } else {
            paginationDiv.append(
              '<button class="page-link" data-page="' +
                i +
                '">' +
                i +
                "</button>"
            );
          }
        }

        if (totalPages > 5 && currentPage + 2 < totalPages) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              totalPages +
              '">' +
              totalPages +
              "</button>"
          );
        }

        if (currentPage < totalPages) {
          paginationDiv.append(
            '<button class="page-link" data-page="' +
              (currentPage + 1) +
              '">Next</button>'
          );
        }
      },
      error: function (error) {
        console.error("Error fetching businesses:", error);
      },
    });
  }

  if ($("#home-listing").length) {
    // Initial load
    loadBusinessesonhomepage(1);

    // Handle pagination click
    $("#pagination").on("click", ".page-link", function () {
      let page = $(this).data("page");
      loadBusinessesonhomepage(page);
    });

    $("#search-filters-form").on("submit", function (event) {
      event.preventDefault();
      loadBusinessesonhomepage(1);
    });
  }

  // Bulk Upload
  $("#create-new-upload").on("click", function () {
    console.log("Clicked");

    let fileInput = $("#data")[0].files[0];

    console.log("Check 1");

    if (!fileInput) {
      $("#action_log").val("Please select a CSV file to upload.");
      return;
    }

    console.log("Check 2");

    if (!fileInput.name.endsWith(".csv")) {
      $("#action_log").val("The selected file is not a CSV file.");
      return;
    }

    console.log("Check 3");

    let formData = new FormData();
    formData.append("file", fileInput);

    console.log("Check 4");

    $.ajax({
      url: "/upload-csv",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        if (response.logs) {
          let logText = "";
          response.logs.forEach(function (log) {
            logText += log + "\n";
          });
          $("#action_log").val(logText);
        } else {
          $("#action_log").val("An error occurred: " + response.error);
        }
      },
      error: function (xhr, status, error) {
        $("#action_log").val("An error occurred: " + xhr.responseText);
      },
    });
  });
});
