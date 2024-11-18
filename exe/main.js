// main.js
const { app, BrowserWindow } = require('electron');

function createWindow() {
    const win = new BrowserWindow({
        width: 766,
        height: 539,
        title: 'Remote RCON 2.0',
        resizable: false,
        webPreferences: {
            nodeIntegration: true, // Enable Node.js integration
            contextIsolation: false // Disable context isolation
        }
    });

    // Load your web application
    win.loadURL('http://77.37.246.6:7777/'); // Replace with your web app URL

    // Remove the menu bar
    win.setMenu(null);

    // Set the zoom factor after the window is ready
    win.webContents.on('did-finish-load', () => {
        win.webContents.setZoomFactor(1.25); // Set zoom factor to 1.25
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});