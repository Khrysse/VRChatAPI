let polling = true;
function pollStatus() {
  if (!polling) return;
  fetch("api/is_current.php?type=connected")
    .then((r) => r.json())
    .then((user) => {
      if (user && user.display_name) {
        document.getElementById("loading").classList.add("hidden");
        document.getElementById("error").classList.add("hidden");
        document.getElementById("connected").classList.remove("hidden");
        document.getElementById("form-login").classList.add("hidden");
        document.getElementById("form-2fa").classList.add("hidden");
        document.getElementById("no-conn").classList.add("hidden");
        document.getElementById("connected-user").innerText = user.display_name;
        document.getElementById("connected-user-id").href =
          "https://vrchat.com/home/user/" + user.user_id;
        document.getElementById("connected-user-id").innerText = user.user_id;
        polling = false; // Stop polling
        return;
      } else {
        document.getElementById("connected").classList.add("hidden");
      }
      // Si pas connecté, poll status/short
      fetch("api/is_current.php?type=status")
        .then((r) => r.json())
        .then((data) => {
          document.getElementById("loading").classList.add("hidden");
          document.getElementById("error").classList.add("hidden");
          let formType = null;
          if (data.status === "NEED_CREDENTIALS")
            formType = "login" && console.log("Hook:", data.status);
          else if (data.status === "NEED_2FA")
            formType = "2fa" && console.log("Hook:", data.status);
          else if (data.status === "CONNECTED")
            formType = null && console.log("Hook:", data.status);
          let showNoConn =
            !formType &&
            data.status !== "CONNECTED" &&
            console.log("Hook:", data.status);
          if (
            formType === "login" ||
            formType === "2fa" ||
            data.status === "CONNECTED"
          ) {
            showNoConn = false;
          }
          document
            .getElementById("form-login")
            .classList.toggle("hidden", formType !== "login");
          document
            .getElementById("form-2fa")
            .classList.toggle("hidden", formType !== "2fa");
          document
            .getElementById("no-conn")
            .classList.toggle("hidden", !showNoConn);
          document.getElementById("last-error").innerText = data.last_error
            ? "Previous error: " + data.last_error
            : "";
        })
        .catch((err) => {
          document.getElementById("loading").classList.add("hidden");
          document.getElementById("error").classList.remove("hidden");
          document.getElementById("error").innerText =
            "Connection error to backend.";
          document.getElementById("form-login").classList.remove("hidden");
          document.getElementById("form-2fa").classList.add("hidden");
          document.getElementById("connected").classList.add("hidden");
          document.getElementById("no-conn").classList.add("hidden");
        });
    });
}
setInterval(pollStatus, 2000);
window.onload = pollStatus;
