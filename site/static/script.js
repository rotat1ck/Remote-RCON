document.addEventListener('DOMContentLoaded', () => {
    const runButton = document.getElementById('run-btn');
    const commandInput = document.getElementById('command-input');
    const terminalOutput = document.getElementById('terminal-output');
    const playerCountElement = document.querySelector('#player-count');
    const playerListContainer = document.querySelector('#player-list-container');
    const logoutButton = document.getElementById('logout-btn');
    const startButton = document.getElementById('start-server');
    const stopButton = document.getElementById('stop-server');

    let accessCode = localStorage.getItem('access_code') || '';
    let players = []; // Array to hold player names

    async function createHash(login, password) {
        // Combine login and password
        const combinedData = login + password;
    
        // Encode the combined data into a Uint8Array
        const encoder = new TextEncoder();
        const data = encoder.encode(combinedData);
    
        // Hash the combined data using SHA-256
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    
        // Send the hash to the server
        return hashHex;
    }

    // Login functionality
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const hashed = await createHash(username, password);
            console.log(hashed);

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ hash: hashed, username: username })
                });

                const result = await response.json();
                if (result.access_code) {
                    accessCode = result.access_code;
                    localStorage.setItem('access_code', accessCode);
                    localStorage.setItem('username', username);
                    window.location.href = '/dashboard';
                } else {
                    alert('Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
            }
        });
    }

    // Retrieve username from local storage
    const username = localStorage.getItem('username') || 'Guest'; // Default to 'Guest' if not found
    const usernameDisplay = document.getElementById('username-display');
    if (usernameDisplay) {
        usernameDisplay.textContent = username; // Set the username in the welcome message
    }

    // Define the addToTerminal function
    function addToTerminal(message, isError = false) {
        const terminalOutput = document.getElementById('terminal-output');
        
        // Create a new div for the message
        const messageDiv = document.createElement('div');
        messageDiv.innerHTML = message; // Set the message content

        // Optionally style the message if it's an error
        if (isError) {
            messageDiv.style.color = 'red'; // Example styling for error messages
        }

        // Append the message to the terminal output
        terminalOutput.appendChild(messageDiv);

        // Scroll to the bottom of the terminal output
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }

    // Function to update player list and dropdowns
    async function updatePlayerList() {
        if (!accessCode) {
            console.error('Access code is not available');
            return;
        }

        try {
            const response = await fetch('/get_players', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ access_code: accessCode }),
            });

            const result = await response.json();
            if (result.players) {
                playerCountElement.textContent = `Players: ${result.total_players || 0}/${result.max_players || 0}`;
                players = result.players; // Store players in the global array

                // Clear previous player list
                playerListContainer.innerHTML = '';

                // Clear action buttons if they exist
                const doxPlayerButtons = document.getElementById('dox-player-buttons');
                const lightPlayerButtons = document.getElementById('light-player-buttons');
                const killPlayerButtons = document.getElementById('kill-player-buttons');
                const banPlayerButtons = document.getElementById('ban-player-buttons');
                const kickPlayerButtons = document.getElementById('kick-player-buttons');

                if (doxPlayerButtons) doxPlayerButtons.innerHTML = '';
                if (lightPlayerButtons) lightPlayerButtons.innerHTML = '';
                if (killPlayerButtons) killPlayerButtons.innerHTML = '';
                if (banPlayerButtons) banPlayerButtons.innerHTML = '';
                if (kickPlayerButtons) kickPlayerButtons.innerHTML = '';

                // Populate player list
                players.forEach(player => {
                    // Create button for player in the main player list
                    const playerButton = document.createElement('button');
                    playerButton.textContent = player;
                    playerButton.classList.add('player-button');
                    playerButton.addEventListener('click', () => {
                        commandInput.value += ' ' + player; // Set command input to the selected player
                    });
                    playerListContainer.appendChild(playerButton);

                    // Create Dox button
                if (doxPlayerButtons) {
                    const doxButton = document.createElement('button');
                    doxButton.textContent = player;
                    doxButton.addEventListener('click', () => {
                        executeCommand(`/dox ${player}`); // Example command
                    });
                    doxPlayerButtons.appendChild(doxButton);
                }

                // Create Light button
                if (lightPlayerButtons) {
                    const lightButton = document.createElement('button');
                    lightButton.textContent = player;
                    lightButton.addEventListener('click', () => {
                        executeCommand(`/light ${player}`); // Example command
                    });
                    lightPlayerButtons.appendChild(lightButton);
                }

                // Create Kill button
                if (killPlayerButtons) {
                    const killButton = document.createElement('button');
                    killButton.textContent = player;
                    killButton.addEventListener('click', () => {
                        executeCommand(`/kill ${player}`); // Example command
                    });
                    killPlayerButtons.appendChild(killButton);
                }

                // Create Ban button
                if (banPlayerButtons) {
                    const banButton = document.createElement('button');
                    banButton.textContent = player;
                    banButton.addEventListener('click', () => {
                        executeCommand(`/ban ${player}`); // Example command
                    });
                    banPlayerButtons.appendChild(banButton);
                }

                // Create Kick button
                if (kickPlayerButtons) {
                    const kickButton = document.createElement('button');
                    kickButton.textContent = player;
                    kickButton.addEventListener('click', () => {
                        executeCommand(`/kick ${player}`); // Example command
                    });
                    kickPlayerButtons.appendChild(kickButton);
                }
            });

                
            } else {
                console.warn('No players found in the response:', result);
            }
        } catch (error) {
            console.error('Error fetching player list:', error);
        }
    }

    

    // Initial player list update
    updatePlayerList();

    // Update player list every 15 seconds
    setInterval(updatePlayerList, 15000);

    // Send command to server
    async function executeCommand(command) {
        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ access_code: accessCode, command })
            });

            const result = await response.json();
            if (response.ok) {
                addToTerminal(`<strong>Command:</strong> ${command}`);
                addToTerminal(`<strong>Output:</strong> ${result.output}`);
            } else {
                addToTerminal(`<strong>Error:</strong> ${result.msg}`, true);
            }
        } catch (error) {
            console.error('Execution error:', error);
            addToTerminal('<strong>Error:</strong> An error occurred while executing the command.', true);
        }
    }

    // Run button event handler
    if (runButton) {
        runButton.addEventListener('click', async () => {
            const command = commandInput.value.trim();
            if (command) {
                await executeCommand(command);
                commandInput.value = ''; // Clear input field
            }
        });
    }

    // Add event listener for Enter key in command input field
    commandInput.addEventListener('keydown', async (event) => {
        if (event.key === 'Enter') { // Check if the pressed key is Enter
            event.preventDefault(); // Prevent the default action (like form submission)
            const command = commandInput.value.trim();
            if (command) {
                await executeCommand(command); // Execute the command
                commandInput.value = ''; // Clear input field
            }
        }
    });

    // Function to hide all action buttons
    function hideAllActionButtons() {
        const trollButtonsContainer = document.getElementById('troll-buttons-container');
        const playersButtonsContainer = document.getElementById('players-buttons-container');
        trollButtonsContainer.style.display = 'none'; // Hide troll buttons
        playersButtonsContainer.style.display = 'none'; // Hide players buttons
    }

    // Function to close all main dropdowns
    function closeAllMainDropdowns() {
        const mainDropdowns = document.querySelectorAll('.dropdown-content');
        mainDropdowns.forEach(dropdown => {
            dropdown.style.display = 'none'; // Hide all main dropdowns
        });
        hideAllActionButtons(); // Also hide action buttons when closing dropdowns
    }

    // Dropdown toggle functionality for main dropdowns
    function toggleMainDropdown(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        const isOpen = dropdown.style.display === 'block'; // Check if the dropdown is already open

        closeAllMainDropdowns(); // Close all main dropdowns first

        // If it was not open, open the selected dropdown
        if (!isOpen) {
            dropdown.style.display = 'block';
        }
    }

    // Function to hide all action buttons
    function hideAllActionButtons() {
        const trollButtonsContainer = document.getElementById('troll-buttons-container');
        const playersButtonsContainer = document.getElementById('players-buttons-container');
        trollButtonsContainer.style.display = 'none'; // Hide troll buttons
        playersButtonsContainer.style.display = 'none'; // Hide players buttons
    }

    // Event listeners for main dropdown buttons
    document.getElementById('toggle-troll-dropdown').addEventListener('click', function() {
        toggleMainDropdown('troll-dropdown');
    });

    document.getElementById('toggle-players-dropdown').addEventListener('click', function() {
        toggleMainDropdown('players-dropdown');
    });

    document.getElementById('toggle-server-dropdown').addEventListener('click', function() {
        toggleMainDropdown('server-dropdown');
    });
    
    // Под-кнопки
    // Event listeners for Troll section buttons
    document.getElementById('toggle-dox-dropdown').addEventListener('click', function() {
        hideAllActionButtons(); // Hide all other buttons
        const actionButtonsContainer = document.getElementById('troll-buttons-container');
        actionButtonsContainer.style.display = 'block'; // Show the troll action buttons container

        // Clear previous buttons
        actionButtonsContainer.innerHTML = '';

        // Populate with Dox buttons
        players.forEach(player => {
            const doxButton = document.createElement('button');
            doxButton.textContent = `${player}`;
            doxButton.addEventListener('click', () => {
                executeCommand(`/dox ${player}`);
                hideAllActionButtons();
            });
            actionButtonsContainer.appendChild(doxButton);
        });
    });

    document.getElementById('toggle-light-dropdown').addEventListener('click', function() {
        hideAllActionButtons(); // Hide all other buttons
        const actionButtonsContainer = document.getElementById('troll-buttons-container');
        actionButtonsContainer.style.display = 'block'; // Show the troll action buttons container

        // Clear previous buttons
        actionButtonsContainer.innerHTML = '';

        // Populate with Light buttons
        players.forEach(player => {
            const lightButton = document.createElement('button');
            lightButton.textContent = `${player}`;
            lightButton.addEventListener('click', () => {
                executeCommand(`/light ${player}`);
                hideAllActionButtons();
            });
            actionButtonsContainer.appendChild(lightButton);
        });
    });

    document.getElementById('toggle-kill-dropdown').addEventListener('click', function() {
        hideAllActionButtons(); // Hide all other buttons
        const actionButtonsContainer = document.getElementById('troll-buttons-container');
        actionButtonsContainer.style.display = 'block'; // Show the troll action buttons container

        // Clear previous buttons
        actionButtonsContainer.innerHTML = '';

        // Populate with Kill buttons
        players.forEach(player => {
            const killButton = document.createElement('button');
            killButton.textContent = `${player}`;
            killButton.addEventListener('click', () => {
                executeCommand(`/kill ${player}`);
                hideAllActionButtons();
            });
            actionButtonsContainer.appendChild(killButton);
        });
    });

    // Event listeners for Players section buttons
    document.getElementById('toggle-ban-dropdown').addEventListener('click', function() {
        hideAllActionButtons(); // Hide all other buttons
        const actionButtonsContainer = document.getElementById('players-buttons-container');
        actionButtonsContainer.style.display = 'block'; // Show the players action buttons container

        // Clear previous buttons
        actionButtonsContainer.innerHTML = '';

        // Populate with Ban buttons
        players.forEach(player => {
            const banButton = document.createElement('button');
            banButton.textContent = `${player}`;
            banButton.addEventListener('click', () => {
                executeCommand(`/ban ${player}`);
                hideAllActionButtons();
            });
            actionButtonsContainer.appendChild(banButton);
        });
    });

    document.getElementById('toggle-kick-dropdown').addEventListener('click', function() {
        hideAllActionButtons(); // Hide all other buttons
        const actionButtonsContainer = document.getElementById('players-buttons-container');
        actionButtonsContainer.style.display = 'block'; // Show the players action buttons container

        // Clear previous buttons
        actionButtonsContainer.innerHTML = '';

        // Populate with Kick buttons
        players.forEach(player => {
            const kickButton = document.createElement('button');
            kickButton.textContent = `${player}`;
            kickButton.addEventListener('click', () => {
                executeCommand(`/kick ${player}`);
                hideAllActionButtons();
            });
            actionButtonsContainer.appendChild(kickButton);
        });
    });
    

    startButton.addEventListener('click', async () => {
        executeCommand(`/start`);
    });
    stopButton.addEventListener('click', async () => {
        executeCommand(`/stop`);
    });
    
    // Logout functionality
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            try {
                const response = await fetch('/logout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ access_code: accessCode })
                });

                const result = await response.json();
                if (result.success) {
                    localStorage.removeItem('access_code');
                    localStorage.removeItem('username');
                    window.location.href = '/';
                }
            } catch (error) {
                console.error('Logout error:', error);
            }
        });
    }


});