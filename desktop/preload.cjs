'use strict';
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('riserDesktop', Object.freeze({
 openProject: () => ipcRenderer.invoke('riser:open'),
 adoptProject: file => ipcRenderer.invoke('riser:adopt', file),
 newProject: () => ipcRenderer.invoke('riser:new'),
 setDirty: dirty => ipcRenderer.invoke('riser:dirty', dirty === true),
 saveProject: request => ipcRenderer.invoke('riser:save', request),
 exportFile: request => ipcRenderer.invoke('riser:export', request),
 exportPdf: () => ipcRenderer.invoke('riser:pdf'),
 onCommand: callback => { const listener = (_event, command) => callback(command); ipcRenderer.on('riser:command', listener); return () => ipcRenderer.removeListener('riser:command', listener); }
}));
