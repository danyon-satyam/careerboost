import { useState } from 'react';

export function usePermissions() {
  const [permissions, setPermissions] = useState({
    camera: false,
    microphone: false,
    screen: false,
    fullscreen: false,
  });
  const [errors, setErrors] = useState({});

  async function requestCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });
      stream.getTracks().forEach(function (t) {
        t.stop();
      });
      setPermissions(function (prev) {
        return Object.assign({}, prev, { camera: true });
      });
      setErrors(function (prev) {
        return Object.assign({}, prev, { camera: null });
      });
      return true;
    } catch {
      setErrors(function (prev) {
        return Object.assign({}, prev, {
          camera: 'Camera access denied. Please allow camera access.',
        });
      });
      return false;
    }
  }

  async function requestMicrophone() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      stream.getTracks().forEach(function (t) {
        t.stop();
      });
      setPermissions(function (prev) {
        return Object.assign({}, prev, { microphone: true });
      });
      setErrors(function (prev) {
        return Object.assign({}, prev, { microphone: null });
      });
      return true;
    } catch {
      setErrors(function (prev) {
        return Object.assign({}, prev, {
          microphone:
            'Microphone access denied. Please allow microphone access.',
        });
      });
      return false;
    }
  }

  async function requestFullscreen() {
    try {
      if (document.documentElement.requestFullscreen) {
        await document.documentElement.requestFullscreen();
      }
      setPermissions(function (prev) {
        return Object.assign({}, prev, { fullscreen: true });
      });
      return true;
    } catch {
      setErrors(function (prev) {
        return Object.assign({}, prev, {
          fullscreen: 'Fullscreen request failed.',
        });
      });
      return false;
    }
  }

  function markScreen() {
    setPermissions(function (prev) {
      return Object.assign({}, prev, { screen: true });
    });
  }

  const allGranted =
    permissions.camera &&
    permissions.microphone &&
    permissions.fullscreen;

  return {
    permissions,
    errors,
    requestCamera,
    requestMicrophone,
    requestFullscreen,
    markScreen,
    allGranted,
  };
}

export default usePermissions;
