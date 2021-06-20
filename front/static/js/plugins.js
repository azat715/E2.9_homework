// Avoid `console` errors in browsers that lack a console.
(function () {
  var method;
  var noop = function () { };
  var methods = [
    'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
    'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
    'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
    'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
  ];
  var length = methods.length;
  var console = (window.console = window.console || {});

  while (length--) {
    method = methods[length];

    // Only stub undefined methods.
    if (!console[method]) {
      console[method] = noop;
    }
  }
}());


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const resModal = new bootstrap.Modal(document.getElementById('Result'), {
  keyboard: false
})

function sendEmail() {
  return {
    csrftoken: getCookie('csrftoken'),
    tab: "list",
    emails: [],
    modal: resModal,
    fetchEmails() {
      fetch('/api/')
        .then(response => response.json())
        .then(data => this.emails = data)
    },
    sendEmail() {
      form = document.getElementById("form");
      formData = new FormData(form);
      fetch('/api/email', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': this.csrftoken
        },
        body: JSON.stringify({
          "subject": formData.get('subject'),
          "message": formData.get('message'),
          "email_to": formData.get('email_to'),
          "timeout": formData.get('timeout'),
        }),
      }).then(() => {
        this.modal.show();
      })
    }
  }
}