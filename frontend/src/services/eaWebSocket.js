// WebSocket service for live EA account and alerts
let socket = null;
let listeners = [];

export const connectEAWebSocket = (onMessage) => {
  if (socket) return;
  socket = new WebSocket("ws://localhost:8000/ws/admin");
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    listeners.forEach((cb) => cb(data));
    if (onMessage) onMessage(data);
  };
  socket.onclose = () => {
    socket = null;
    listeners = [];
  };
};

export const subscribeEAUpdates = (cb) => {
  listeners.push(cb);
};

export const disconnectEAWebSocket = () => {
  if (socket) socket.close();
  socket = null;
  listeners = [];
};
