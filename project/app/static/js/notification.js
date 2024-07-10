function showNotification(title, description, type) {
  var notification = $(`
        <div class="notification notification-${type}">
            <div class="notification-title">${title}</div>
            <div class="notification-description">${description}</div>
            <div class="loading-bar"></div>
        </div>
    `);

  $("#notification-container").append(notification);

  // Animate the loading bar
  notification.find(".loading-bar").css("animation", "loading 3s linear");

  notification
    .fadeIn(500)
    .delay(3000)
    .fadeOut(500, function () {
      $(this).remove();
    });
}
