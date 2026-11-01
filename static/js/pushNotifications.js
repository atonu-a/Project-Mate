import { initializeApp } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-app.js";
import {
  getMessaging,
  getToken,
  isSupported,
  onMessage,
} from "https://www.gstatic.com/firebasejs/13.0.0/firebase-messaging.js";

const button = document.getElementById("enable-push-notifications");

if (button) {
  const status = document.getElementById("push-notifications-status");
  const csrfToken = document.querySelector(
    "#push-notifications-csrf input[name='csrfmiddlewaretoken']",
  )?.value;
  const firebaseConfig = {
    apiKey: "AIzaSyAgPUBpLsqhOl43M-6FZLNbjMuuqxC-Kx8",
    authDomain: "projectmate-5082f.firebaseapp.com",
    projectId: "projectmate-5082f",
    storageBucket: "projectmate-5082f.firebasestorage.app",
    messagingSenderId: "746046640690",
    appId: "1:746046640690:web:395f5cd2bc18b5e88aa22b",
    measurementId: "G-ZTSN049QX8",
  };
  const vapidKey =
    "BDhXbiLcNFEX7E3GAZFXDLT8A12kbVAjWjoc4O6bMWbVZsYrpQJaxKBi3Nj22Ks_pmrr7gidtxu9M3BH6ERUvCI";

  const setStatus = (message) => {
    status.textContent = message;
  };

  const safeNotificationUrl = (value) => {
    const url = new URL(value || "/notifications/", window.location.origin);
    return url.origin === window.location.origin ? url.href : "/notifications/";
  };

  const setupPushNotifications = async () => {
    if (
      !window.isSecureContext ||
      !("Notification" in window) ||
      !("serviceWorker" in navigator) ||
      !csrfToken
    ) {
      button.disabled = true;
      setStatus("Push notifications are unavailable in this browser or connection.");
      return;
    }

    try {
      if (!(await isSupported())) {
        button.disabled = true;
        setStatus("Push notifications are not supported by this browser.");
        return;
      }

      const app = initializeApp(firebaseConfig);
      const messaging = getMessaging(app);
      const serviceWorkerRegistration = await navigator.serviceWorker.register(
        "/static/firebase-msg-sw.js",
      );

      onMessage(messaging, ({ data = {} }) => {
        if (Notification.permission !== "granted" || !data.title) {
          return;
        }

        const notification = new Notification(data.title, {
          body: data.body || "",
        });
        notification.onclick = () => {
          window.location.assign(safeNotificationUrl(data.url));
        };
      });

      button.addEventListener("click", async () => {
        button.disabled = true;
        setStatus("");

        try {
          const permission =
            Notification.permission === "granted"
              ? "granted"
              : await Notification.requestPermission();
          if (permission !== "granted") {
            setStatus("Allow notifications in your browser to enable push.");
            return;
          }

          const fcmToken = await getToken(messaging, {
            vapidKey,
            serviceWorkerRegistration,
          });
          if (!fcmToken) {
            throw new Error("Firebase did not return a registration token.");
          }

          const response = await fetch(button.dataset.saveUrl, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ fcm_token: fcmToken }),
          });
          if (!response.ok || response.redirected) {
            throw new Error(`Saving the push token failed (${response.status}).`);
          }

          button.textContent = "Push notifications enabled";
          setStatus("This browser can now receive notifications.");
        } catch (error) {
          console.error("Could not enable push notifications:", error);
          setStatus("Could not enable push notifications. Please try again.");
        } finally {
          button.disabled = false;
        }
      });
    } catch (error) {
      console.error("Could not initialize push notifications:", error);
      button.disabled = true;
      setStatus("Push notifications could not be initialized.");
    }
  };

  setupPushNotifications();
}
