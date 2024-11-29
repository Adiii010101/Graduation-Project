importScripts('/__/firebase/9.2.0/firebase-app-compat.js');
importScripts('/__/firebase/9.2.0/firebase-messaging-compat.js');
importScripts('/__/firebase/init.js');

importScripts('https://www.gstatic.com/firebasejs/9.2.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.2.0/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyD2FEhA0BmiS1yM-eoAoaoeqYPGRp4ZEEs",
    authDomain: "fire-base-notification-5b37d.firebaseapp.com",
    projectId: "fire-base-notification-5b37d",
    storageBucket: "fire-base-notification-5b37d.appspot.com",
    messagingSenderId: "596038722714",
    appId: "1:596038722714:web:41d1ae1b3baad1979eab23",
    measurementId: "G-J4VPHXVR7P"
 });

 const messaging = firebase.messaging();

 
 // https://firebase.google.com/docs/cloud-messaging/concept-options
 messaging.onBackgroundMessage(function(payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    // Customize notification here
    const notificationTitle = 'Background Message Title';
  //   const notificationOptions = {
  //     body: 'Background Message body.',
  //     // icon: '/firebase-logo.png'
  //   };
  
    self.registration.showNotification(notificationTitle);
  });