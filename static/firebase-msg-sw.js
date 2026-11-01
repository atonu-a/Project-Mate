importScripts(
  "https://www.gstatic.com/firebasejs/13.0.0/firebase-app-compat.js",
);
importScripts(
  "https://www.gstatic.com/firebasejs/13.0.0/firebase-messaging-compat.js",
);

firebase.initializeApp({
  apiKey: "AIzaSyAgPUBpLsqhOl43M-6FZLNbjMuuqxC-Kx8",
  authDomain: "projectmate-5082f.firebaseapp.com",
  projectId: "projectmate-5082f",
  storageBucket: "projectmate-5082f.firebasestorage.app",
  messagingSenderId: "746046640690",
  appId: "1:746046640690:web:395f5cd2bc18b5e88aa22b",
  measurementId: "G-ZTSN049QX8",
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(({ data = {} }) => {
  self.registration.showNotification(data.title || "ProjectMate", {
    body: data.body || "You have a new notification.",
    data: { url: data.url || "/notifications/" },
  });
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const target = new URL(
    event.notification.data?.url || "/notifications/",
    self.location.origin,
  );
  const targetUrl =
    target.origin === self.location.origin ? target.href : "/notifications/";
  event.waitUntil(self.clients.openWindow(targetUrl));
});
