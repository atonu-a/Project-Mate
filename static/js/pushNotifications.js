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
  const isIosDevice =
    /iPhone|iPad|iPod/i.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  let messaging;
  let serviceWorkerRegistration;

  const setStatus = (message) => {
    status.textContent = message;
  };

  const safeNotificationUrl = (value) => {
    const url = new URL(value || "/notifications/", window.location.origin);
    return url.origin === window.location.origin ? url.href : "/notifications/";
  };

  button.disabled = true;
  button.addEventListener("click", async () => {
    if (!messaging || !serviceWorkerRegistration) {
      setStatus("Push notifications are still getting ready. Please wait a moment.");
      return;
    }

    button.disabled = true;
    setStatus("Waiting for notification permission...");

    try {
      const permission =
        Notification.permission === "granted"
          ? "granted"
          : await Notification.requestPermission();
      if (permission !== "granted") {
        setStatus("Allow notifications in your browser to enable push.");
        return;
      }

      setStatus("Registering this browser for push notifications...");
      const fcmToken = await getToken(messaging, {
        vapidKey,
        serviceWorkerRegistration,
      });
      if (!fcmToken) {
        throw new Error("Firebase did not return a registration token.");
      }

      setStatus("Saving this browser's notification settings...");
      const response = await fetch(button.dataset.saveUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ fcm_token: fcmToken }),
      });
      if (response.redirected) {
        throw new Error("Your sign-in may have expired. Sign in again and retry.");
      }
      const result = await response.json();
      if (!response.ok) {
        throw new Error(
          result.error ||
            `The server could not verify push delivery (${response.status}).`,
        );
      }

      button.textContent = "Push notifications enabled";
      setStatus(
        `${result.message} Check that the test notification appeared; future notifications require the site to be allowed by your browser.`,
      );
    } catch (error) {
      console.error("Could not enable push notifications:", error);
      const errorCode = error?.code ? ` (${error.code})` : "";
      const isPushServiceError =
        error?.name === "AbortError" || error?.code === 20;
      const message = isPushServiceError
        ? "The browser push service rejected the subscription. In Brave, enable Settings > Privacy and security > Use Google Services for Push Messaging, then reload and retry. A VPN, firewall, or content blocker may also be blocking push."
        : error?.message || "An unexpected error occurred.";
      setStatus(`Could not enable push notifications${errorCode}: ${message}`);
    } finally {
      button.disabled = false;
    }
  });

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

    if (
      isIosDevice &&
      !window.matchMedia("(display-mode: standalone)").matches &&
      !navigator.standalone
    ) {
      button.disabled = true;
      setStatus(
        "On iPhone or iPad, add this website to your Home Screen and open it there to enable push notifications.",
      );
      return;
    }

    try {
      setStatus("Preparing push notifications...");
      if (!(await isSupported())) {
        button.disabled = true;
        setStatus(
          "Push notifications are not supported in this browser. Try a supported browser over HTTPS.",
        );
        return;
      }

      const app = initializeApp(firebaseConfig);
      messaging = getMessaging(app);
      serviceWorkerRegistration = await navigator.serviceWorker.register(
        "/firebase-messaging-sw.js",
      );

      onMessage(messaging, ({ data = {} }) => {
        if (Notification.permission !== "granted" || !data.title) {
          return;
        }

        serviceWorkerRegistration
          .showNotification(data.title, {
            body: data.body || "",
            data: { url: safeNotificationUrl(data.url) },
          })
          .catch((error) => {
            console.error("Could not show foreground notification:", error);
          });
      });

      button.disabled = false;
      setStatus("");
    } catch (error) {
      console.error("Could not initialize push notifications:", error);
      button.disabled = true;
      const errorCode = error?.code ? ` (${error.code})` : "";
      const message =
        error?.message || "Check that the push service worker is available.";
      setStatus(
        `Push notifications could not be initialized${errorCode}: ${message}`,
      );
    }
  };

  setupPushNotifications();
}
